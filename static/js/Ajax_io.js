/* * PollingClient.js
 * This module provides a PollingClient class that allows for periodic polling of a given URL.
    * It uses the Fetch API to make GET requests and dispatches events based on the response.
    * It can also handle errors and allows for starting and stopping the polling process.
    * Usage:
    * const client = new PollingClient('https://example.com/api', 5000);
    * client.addEventListener('data_event', (event) => {
    *    console.log('Data received:', event.detail);
    * });
    * client.start();
    * client.stop();
*/

export class PollingClient extends EventTarget {
    constructor(url, interval = 3000, onError = null) {
        super();
        this.url = url;
        this.interval = interval;
        this.onError = onError;
        this.timer = null;
        this.controller = null;
    }

    start() {
        if (this.timer) return; // Already running
        this.timer = setInterval(() => this._poll(), this.interval);
        this._poll(); // Otherwise, start polling
        // If you want to start with a POST request instead of GET, uncomment the line below
        // this._post(); // Start with a POST request
        
    }

    async _poll() {
        try {
            if (this.controller) this.controller.abort();
            this.controller = new AbortController();

            const res = await fetch(this.url, { signal: this.controller.signal });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();

            if (data.event) {
                this.dispatchEvent(new CustomEvent(data.event, { detail: data.payload }));
            } else {
                this.dispatchEvent(new CustomEvent('no_event', { detail: data }));
            }

        } catch (err) {
            if (err.name !== 'AbortError') {
                console.error('Polling error:', err);
                if (typeof this.onError === 'function') {
                    this.onError(err);
                }
            }
        }
    }
    
    stop() {
        clearInterval(this.timer);
        this.timer = null;
        if (this.controller) this.controller.abort();
    }

    isRunning() {
        return this.timer !== null;
    }
}