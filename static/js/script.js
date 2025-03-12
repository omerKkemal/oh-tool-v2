let command = ['help','clear','api-link','delet','reconnect'] // reconnect and api-link are from the same databse table

async function api(endPoint,data,method_){
    if (method_ === 'delet'){
        const result = await fetch(window.location.host+endPoint,{
            method:method_,
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({'id':ID})
        });
        return result;

    }
    else if(method_ === 'get'){
        try{
            const respons = await fetch(window.location.host+endPoint);
            const result = await respons.json();
            return result
        } catch{
            console.error('Error: ',error);
            return null;
        }
        
    }else if(method_ === 'post' && data !== null){
        try{
            const result = await fetch(window.location.host+endPoint,{
                method: method_,
                headers: {
                    'Content-Type':'application/json'
                },
                body:JSON.stringify(data)
            });
            return await result.json();
        } catch{
            console.error('Error: ',error);
            return null;         
        }

    }
}

function help_cmd(inputText){
    if (inputText[0] === 'help'){
        return `this is help message<br>-----------------------
                Commands                                       Use.
                ------------------------------------------------
                help                                         :  show this help message.
                clear                                        :  clear the screen.
                api-link                                   :  list all avilble api likes.
                delet                                        :  used to edit commands(delet).
                reconnect                              :  used to reconnect to the netcat or chenge connection
                                                                      (chenge to api command or to netcat).`
    }else if(inputText[0] === 'api-link' && inputText[1] === 'help'){
        return `${inputText[0]} [command [option]]<br>
        commands
            [*] help
            [*] update
            [*] delete
        update [-i,--id], [-l,--link]
        update [-i,--id], [-a,--action]
        delete [-i,--id]<br>
        Note: you can use the api like web gui to update or to delete,when you use update command you can use two option if you want,
        or all three option but id must be used `
    }
}

document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        let inputText = this.value.trim();
        if (inputText === '') return;

        let terminal = document.getElementById('terminal');

        // Create a new line with user input
        let newLine = document.createElement('div');
        newLine.classList.add('line');
        newLine.innerHTML = `<span class="prompt">$</span> <span>${inputText}</span>`;
        terminal.insertBefore(newLine, this.parentElement);

        // Create loading animation
        let loadingLine = document.createElement('div');
        loadingLine.classList.add('line');
        loadingLine.innerHTML = `<span class="prompt"></span> <span class="loading"></span>`;
        terminal.insertBefore(loadingLine, this.parentElement);

        this.value = '';
        terminal.scrollTop = terminal.scrollHeight;

        // Increase height dynamically
        if (terminal.scrollHeight > terminal.clientHeight) {
            terminal.style.maxHeight = terminal.scrollHeight + 'px';
        }
        // Simulate processing for 3 seconds, then replace loading with output
        
        if (command.includes(inputText.split(' ')[0])){
            loadingLine.innerHTML = `<span class="px-4 prompt"></span><span style="white-space:pre;">${help_cmd(inputText.split(' '))}</span>`;
            terminal.scrollTop = terminal.scrollHeight;
            
        }else{
            loadingLine.innerHTML = `<span class="prompt"></span><span>Processed: ${inputText}</span>`;
            terminal.scrollTop = terminal.scrollHeight;
        }

    }
});