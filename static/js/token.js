function copyToClipboard(text) {
            const tempElement = document.createElement('textarea');
            tempElement.value = text;
            document.body.appendChild(tempElement);
            tempElement.select();
            document.execCommand('copy');
            document.body.removeChild(tempElement);

            console.log("Text copied: ", text);

            window.location.href = "/";
        }