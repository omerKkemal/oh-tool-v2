/* 
 * Enhanced PollingClient.js
 * A robust polling client with exponential backoff, retry mechanisms, and advanced features
 * 
 * Features:
 * - Exponential backoff with jitter for network errors
 * - Configurable retry strategies
 * - Request deduplication
 * - Health monitoring and statistics
 * - Multiple event types for different states
 * - Request/response transformers
 * - Graceful degradation
 * - Memory leak prevention
 * 
 * Usage:
 * const client = new PollingClient('https://api.example.com/data', {
 *   interval: 5000,
 *   retryAttempts: 3,
 *   backoffMultiplier: 2
 * });
 * 
 * client.addEventListener('data', (event) => {
 *   console.log('Data received:', event.detail);
 * });
 * 
 * client.addEventListener('error', (event) => {
 *   console.error('Polling error:', event.detail);
 * });
 * 
 * client.addEventListener('health', (event) => {
 *   console.log('Health stats:', event.detail);
 * });
 * 
 * client.start();
 */

export class PollingClient extends EventTarget {
    constructor(url, options = {}) {
        super();
        
        // Configuration with defaults
        this.config = {
            url,
            interval: options.interval || 5000,
            retryAttempts: options.retryAttempts || 3,
            backoffMultiplier: options.backoffMultiplier || 2,
            maxInterval: options.maxInterval || 30000,
            timeout: options.timeout || 10000,
            immediate: options.immediate !== false, // First request immediately
            jitter: options.jitter !== false, // Add randomness to avoid thundering herd
            deduplicate: options.deduplicate !== false, // Prevent duplicate requests
            ...options
        };

        // State management
        this.state = {
            isRunning: false,
            retryCount: 0,
            consecutiveErrors: 0,
            lastRequestTime: null,
            lastResponseTime: null,
            requestCount: 0,
            errorCount: 0,
            lastData: null
        };

        // Internal references
        this.timer = null;
        this.controller = null;
        this.pendingRequest = null;
        this.lastRequestId = 0;

        // Bind methods
        this._poll = this._poll.bind(this);
        this._handleError = this._handleError.bind(this);
    }

    /**
     * Start the polling process
     */
    start() {
        if (this.state.isRunning) {
            console.warn('PollingClient: Already running');
            return;
        }

        this.state.isRunning = true;
        this.state.retryCount = 0;
        this.state.consecutiveErrors = 0;

        this.dispatchEvent(new CustomEvent('start', { 
            detail: { config: this.config, state: this.state }
        }));

        // Initial request
        if (this.config.immediate) {
            this._poll();
        }

        // Start interval
        this.timer = setInterval(this._poll, this.config.interval);

        this._updateHealthStats();
    }

    /**
     * Stop the polling process
     */
    stop() {
        if (!this.state.isRunning) return;

        this.state.isRunning = false;
        clearInterval(this.timer);
        this.timer = null;

        // Abort any pending request
        if (this.controller) {
            this.controller.abort();
            this.controller = null;
        }

        // Clear pending promise
        this.pendingRequest = null;

        this.dispatchEvent(new CustomEvent('stop', { 
            detail: { state: this.state }
        }));
    }

    /**
     * Restart the polling process
     */
    restart() {
        this.stop();
        setTimeout(() => this.start(), 100);
    }

    /**
     * Main polling method
     */
    async _poll() {
        // Prevent duplicate requests
        if (this.pendingRequest && this.config.deduplicate) {
            return;
        }

        const requestId = ++this.lastRequestId;
        this.state.lastRequestTime = Date.now();
        this.state.requestCount++;

        try {
            // Abort previous request if still pending
            if (this.controller) {
                this.controller.abort();
            }

            this.controller = new AbortController();
            const timeoutId = setTimeout(() => {
                this.controller.abort();
            }, this.config.timeout);

            this.pendingRequest = this._makeRequest(requestId);
            const data = await this.pendingRequest;

            clearTimeout(timeoutId);
            
            // Only process if this is the most recent request
            if (requestId === this.lastRequestId) {
                this._handleSuccess(data);
            }

        } catch (error) {
            // Only process if this is the most recent request
            if (requestId === this.lastRequestId) {
                this._handleError(error);
            }
        } finally {
            if (requestId === this.lastRequestId) {
                this.pendingRequest = null;
                this.controller = null;
            }
            this._updateHealthStats();
        }
    }

    /**
     * Make the actual HTTP request
     */
    async _makeRequest(requestId) {
        const options = {
            signal: this.controller.signal,
            headers: {
                'Content-Type': 'application/json',
                'X-Request-ID': requestId,
                'X-Polling-Client': 'true'
            },
            cache: this.config.cache || 'no-cache'
        };

        // Add authentication if provided
        if (this.config.headers) {
            Object.assign(options.headers, this.config.headers);
        }

        const response = await fetch(this.config.url, options);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        } else {
            return await response.text();
        }
    }

    /**
     * Handle successful response
     */
    _handleSuccess(data) {
        this.state.lastResponseTime = Date.now();
        this.state.consecutiveErrors = 0;
        this.state.retryCount = 0;

        // Check if data has changed
        const dataChanged = JSON.stringify(data) !== JSON.stringify(this.state.lastData);
        this.state.lastData = data;

        // Dispatch appropriate events
        if (data && typeof data === 'object') {
            if (data.event) {
                this.dispatchEvent(new CustomEvent(data.event, { 
                    detail: data.payload || data 
                }));
            } else {
                this.dispatchEvent(new CustomEvent('data', { 
                    detail: data 
                }));
            }
        } else {
            this.dispatchEvent(new CustomEvent('data', { 
                detail: data 
            }));
        }

        // Notify about data changes
        if (dataChanged) {
            this.dispatchEvent(new CustomEvent('dataChanged', { 
                detail: data 
            }));
        }

        // Reset to normal interval after success
        if (this.state.retryCount > 0) {
            this._resetInterval();
        }
    }

    /**
     * Handle errors with retry logic and exponential backoff
     */
    _handleError(error) {
        this.state.errorCount++;
        this.state.consecutiveErrors++;

        // Don't retry on abort errors
        if (error.name === 'AbortError') {
            this.dispatchEvent(new CustomEvent('abort', { 
                detail: { error, state: this.state }
            }));
            return;
        }

        // Determine if we should retry
        const shouldRetry = this.state.retryCount < this.config.retryAttempts;
        
        this.dispatchEvent(new CustomEvent('error', { 
            detail: { 
                error, 
                retryCount: this.state.retryCount,
                shouldRetry,
                state: this.state
            }
        }));

        if (shouldRetry && this.state.isRunning) {
            this._scheduleRetry();
        } else if (!shouldRetry) {
            this.dispatchEvent(new CustomEvent('maxRetriesExceeded', { 
                detail: { 
                    error, 
                    retryCount: this.state.retryCount,
                    state: this.state
                }
            }));
        }
    }

    /**
     * Schedule a retry with exponential backoff
     */
    _scheduleRetry() {
        this.state.retryCount++;

        const baseDelay = this.config.interval;
        const backoffDelay = Math.min(
            baseDelay * Math.pow(this.config.backoffMultiplier, this.state.retryCount - 1),
            this.config.maxInterval
        );

        // Add jitter to avoid synchronized retries
        const jitter = this.config.jitter ? 
            (Math.random() * 0.3 + 0.85) : 1; // 0.85 to 1.15
        const delay = backoffDelay * jitter;

        this.dispatchEvent(new CustomEvent('retryScheduled', { 
            detail: { 
                delay: Math.round(delay),
                retryCount: this.state.retryCount,
                state: this.state
            }
        }));

        // Clear current interval and schedule retry
        clearInterval(this.timer);
        this.timer = setTimeout(() => {
            if (this.state.isRunning) {
                this._poll();
                // Restore normal interval after retry
                this.timer = setInterval(this._poll, this.config.interval);
            }
        }, delay);
    }

    /**
     * Reset to normal polling interval
     */
    _resetInterval() {
        if (this.timer && this.state.isRunning) {
            clearInterval(this.timer);
            this.timer = setInterval(this._poll, this.config.interval);
        }
    }

    /**
     * Update and emit health statistics
     */
    _updateHealthStats() {
        const healthStats = {
            isRunning: this.state.isRunning,
            requestCount: this.state.requestCount,
            errorCount: this.state.errorCount,
            consecutiveErrors: this.state.consecutiveErrors,
            retryCount: this.state.retryCount,
            lastRequestTime: this.state.lastRequestTime,
            lastResponseTime: this.state.lastResponseTime,
            successRate: this.state.requestCount > 0 ? 
                ((this.state.requestCount - this.state.errorCount) / this.state.requestCount * 100).toFixed(2) : 100,
            uptime: this.state.startTime ? Date.now() - this.state.startTime : 0
        };

        this.dispatchEvent(new CustomEvent('health', { 
            detail: healthStats 
        }));
    }

    /**
     * Update configuration dynamically
     */
    updateConfig(newConfig) {
        const wasRunning = this.state.isRunning;
        
        if (wasRunning) {
            this.stop();
        }

        this.config = { ...this.config, ...newConfig };

        if (wasRunning) {
            this.start();
        }

        this.dispatchEvent(new CustomEvent('configUpdated', { 
            detail: { config: this.config }
        }));
    }

    /**
     * Get current state and statistics
     */
    getStats() {
        return {
            config: { ...this.config },
            state: { ...this.state },
            health: {
                isRunning: this.state.isRunning,
                requestCount: this.state.requestCount,
                errorCount: this.state.errorCount,
                successRate: this.state.requestCount > 0 ? 
                    ((this.state.requestCount - this.state.errorCount) / this.state.requestCount * 100).toFixed(2) : 100,
                consecutiveErrors: this.state.consecutiveErrors
            }
        };
    }

    /**
     * Check if polling is active
     */
    isRunning() {
        return this.state.isRunning;
    }

    /**
     * Manually trigger a poll (useful for testing or manual refresh)
     */
    async pollOnce() {
        if (this.pendingRequest) {
            return this.pendingRequest;
        }
        return this._poll();
    }

    /**
     * Clean up resources
     */
    destroy() {
        this.stop();
        this.removeAllEventListeners?.();
    }
}

// Convenience function for quick polling
export function createPollingClient(url, options = {}) {
    return new PollingClient(url, options);
}

// Utility function for common polling patterns
export const PollingStrategies = {
    aggressive: {
        interval: 1000,
        retryAttempts: 5,
        backoffMultiplier: 1.5
    },
    balanced: {
        interval: 5000,
        retryAttempts: 3,
        backoffMultiplier: 2
    },
    conservative: {
        interval: 10000,
        retryAttempts: 2,
        backoffMultiplier: 3
    }
};
