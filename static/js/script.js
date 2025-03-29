let commands = ['help', 'clear', 'api-link', 'delete', 'reconnect','get','reload']; // Fixed spelling
let endPoints = ['/api_command', '/api_link'];

function cmd(userInput) {
    let input = userInput.split(' ');
    console.log(input);

    if (input[0] === "api-link") {
        if (input.includes('-i') || input.includes('--id')) {
            if (input.length === 6) {
                if (input[1] === 'update') {
                    if ((input[2] === '-i' || input[2] === '--id') &&
                        (input[4] === '-a' || input[4] === '--action')) {
                        return `api-link update action`;
                    }
                    if ((input[2] === '-i' || input[2] === '--id') &&
                        (input[4] === '-l' || input[4] === '--link')) {
                        return `api-link update link`;
                    }
                }
            } else if (input[1] === 'delete' && input.length === 4) {
                return `api-link delete`;
            }
        }else if(input.length === 2 && input[1] === 'help'){
            return help_cmd(input);
        }else{
            return `Please provide correct options`;
        }
    }else if(input[0] === 'get'){
        api('/api_command/api',NaN,'get').then(data => console.log(data));
    }else if(input.length == 1 && input[0] === 'reload'){
        window.location.reload();
    }else{
        return help_cmd(input)
    }
}

async function api(endPoint, data, method) {
    try {
        let options = {
            method: method.toUpperCase(),
            headers: { 'Content-Type': 'application/json' },
        };

        if (method.toLowerCase() !== 'get') {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(window.location.origin + endPoint, options);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

function help_cmd(inputText) {
    if (inputText[0] === 'help') {
        return `This is help message<br>-----------------------
                Commands                                       Use.
                ------------------------------------------------
                help                                         :  Show this help message.
                clear                                        :  Clear the screen.
                api-link                                   :  List all available API links.
                delete                                       :  Used to edit commands (delete).
                reconnect                              :  Used to reconnect to the netcat or change connection
                                                                  (change to API command or to netcat).`;
    } else if (inputText[0] === 'api-link' && inputText[1] === 'help') {
        return `${inputText[0]} [command [option]]<br>
        Commands
            [*] help
            [*] update
            [*] delete
        update [-i,--id], [-l,--link]
        update [-i,--id], [-a,--action]
        delete [-i,--id]<br>
        Note: You can use the API-like web GUI to update or delete. When using the update command, you can use two options
        or all three, but ID must be used.`;
    }
}

document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        let inputText = this.value.trim();
        if (inputText === '') return;

        let terminal = document.getElementById('terminal');

        let newLine = document.createElement('div');
        newLine.classList.add('line');
        newLine.innerHTML = `<span class="prompt">$</span> <span>${inputText}</span>`;
        terminal.insertBefore(newLine, this.parentElement);

        let loadingLine = document.createElement('div');
        loadingLine.classList.add('line');
        loadingLine.innerHTML = `<span class="prompt"></span> <span class="loading"></span>`;
        terminal.insertBefore(loadingLine, this.parentElement);

        this.value = '';
        terminal.scrollTop = terminal.scrollHeight;

        if (terminal.scrollHeight > terminal.clientHeight) {
            terminal.style.maxHeight = terminal.scrollHeight + 'px';
        }

        let inputCommand = inputText.split(' ')[0];

        if (commands.includes(inputCommand)) {
            loadingLine.innerHTML = `<span class="px-4 prompt"></span><span style="white-space:pre;">${cmd(inputText)}</span>`;
        } else {
            loadingLine.innerHTML = `<span class="prompt"></span><span>Processing: ${inputText}</span>`;
            let data = { input : inputText };
            api(endPoints[0], data, 'POST').then(_data => console.log(_data));
        }

        terminal.scrollTop = terminal.scrollHeight;
    }
});
