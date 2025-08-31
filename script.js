document.addEventListener('DOMContentLoaded', () => {
    const processButton = document.getElementById('processButton');
    const inputText = document.getElementById('inputText');
    const statusMessage = document.getElementById('statusMessage');

    processButton.addEventListener('click', async () => {
        const text = inputText.value.trim();

        if (text === '') {
            statusMessage.textContent = '文章を入力してください。';
            statusMessage.style.color = 'red';
            return;
        }

        statusMessage.textContent = '処理中です...';
        statusMessage.style.color = '#666';

        try {
            const response = await fetch('/create-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'kanji_list.pdf';
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                statusMessage.textContent = 'PDFが正常に作成されました。';
                statusMessage.style.color = 'green';
            } else {
                const error = await response.json();
                statusMessage.textContent = `エラー: ${error.error || response.statusText}`;
                statusMessage.style.color = 'red';
            }
        } catch (error) {
            statusMessage.textContent = 'サーバーとの通信に失敗しました。';
            statusMessage.style.color = 'red';
        }
    });
});