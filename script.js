document.addEventListener('DOMContentLoaded', () => {
    const processButton = document.getElementById('processButton');
    const inputText = document.getElementById('inputText');
    const statusMessage = document.getElementById('statusMessage');

    processButton.addEventListener('click', () => {
        const text = inputText.value.trim();

        if (text === '') {
            statusMessage.textContent = '文章を入力してください。';
            statusMessage.style.color = 'red';
            return;
        }

        statusMessage.textContent = '処理中です...';
        statusMessage.style.color = '#666';

        // 開発者向け: 実際の通信がないため、数秒後に完了メッセージを表示
        setTimeout(() => {
            statusMessage.textContent = 'PDF作成リクエストを送信しました！';
            statusMessage.style.color = 'green';
        }, 2000);
    });
});