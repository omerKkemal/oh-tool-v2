const commands = ['help', 'clear', 'api-link', 'delete', 'reconnect', 'get', 'reload'];

document.getElementById('userInput').addEventListener('keypress', async function (event) {
    if (event.key === 'Enter') {
        let inputText = this.value.trim();
        if (!inputText) return;

        let terminal = document.getElementById('terminal');

        // Show user input
        let newLine = document.createElement('div');
        newLine.classList.add('line');
        newLine.innerHTML = `<span class="prompt">$</span> <span>${escapeHtml(inputText)}</span>`;
        terminal.insertBefore(newLine, this.parentElement);

        // Placeholder for command output
        let outputLine = document.createElement('div');
        outputLine.classList.add('line');
        outputLine.innerHTML = `<span class="prompt">$</span> <span class="loading">...</span>`;
        terminal.insertBefore(outputLine, this.parentElement);

        this.value = '';
        terminal.scrollTop = terminal.scrollHeight;

        let inputCommand = inputText.split(' ')[0];

        if (commands.includes(inputCommand)) {
            try {
                const result = await cmd(inputText);
                outputLine.innerHTML = `<span class="prompt"></span><span style="white-space:pre;">${escapeHtml(result || 'Done')}</span>`;
            } catch (e) {
                outputLine.innerHTML = `<span class="prompt"></span><span>Error: ${escapeHtml(e.message)}</span>`;
            }
        } else {
            // Send unknown commands to server API
            const data = { input: inputText };
            const response = await api(data, 'POST');
            const msg = (response && response.response) || response?.message || 'Done';
            outputLine.innerHTML = `<span class="prompt"></span><span>${escapeHtml(msg)}</span>`;
        }

        terminal.scrollTop = terminal.scrollHeight;
    }
});

async function cmd(userInput) {
    const input = userInput.split(' ');
    console.log(input);

    if (input[0] === "api-link") {
        if (input.includes('-i') || input.includes('--id')) {
            if (input.length === 6 && input[1] === 'update') {
                if ((input[2] === '-i' || input[2] === '--id') &&
                    (input[4] === '-a' || input[4] === '--action')) {
                    return `api-link update action`;
                }
                if ((input[2] === '-i' || input[2] === '--id') &&
                    (input[4] === '-l' || input[4] === '--link')) {
                    return `api-link update link`;
                }
            } else if (input[1] === 'delete' && input.length === 4) {
                return `api-link delete`;
            }
        } else if (input.length === 2 && input[1] === 'help') {
            return help_cmd(input);
        } else {
            return `Please provide correct options`;
        }
    } else if (input[0] === 'get') {
        const data = await api(null, 'get', '/api_command/api');
        return JSON.stringify(data, null, 2);
    } else if (input.length === 1 && input[0] === 'reload') {
        window.location.reload();
    } else {
        return help_cmd(input);
    }
}

async function api(data, method, parm = '') {
    try {
        let options = {
            method: method.toUpperCase(),
            headers: { 'Content-Type': 'application/json' },
        };

        if (method.toLowerCase() !== 'get' && data) {
            options.body = JSON.stringify(data);
        }

        let url = window.location.href;
        if (url.endsWith('/')) url = url.slice(0, -1);
        if (parm && typeof parm === 'string') {
            url += parm.startsWith('/') ? parm : '/' + parm;
        }

        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        alert(error);
        console.error('API Error:', error);
        return null;
    }
}

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
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
