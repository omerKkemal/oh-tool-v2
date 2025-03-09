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
        setTimeout(() => {
            if (inputText === 'help'){
                loadingLine.innerHTML = `<span class="px-4 prompt"></span><span><h6 class="text-center">this is help message<br>-----------------------</h6>
                <br>help  ____________________ : display this help message
                <br>clear ____________________ : clear the screen</span>`;
                terminal.scrollTop = terminal.scrollHeight;
            
            }else{
                loadingLine.innerHTML = `<span class="prompt"></span><span>Processed: ${inputText}</span>`;
                terminal.scrollTop = terminal.scrollHeight;
            }
        }, 3000);
    }
});