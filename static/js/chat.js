function scrollToBottom(){
	const messages=document.getElementById("message-area")
	messages.scrollTop = messages.scrollHeight;
}



function formatAMPM(date) {
	var hours = date.getHours();
	var minutes = date.getMinutes();
	var ampm = hours >= 12 ? 'PM' : 'AM';
	hours = hours % 12;
	hours = hours ? hours : 12;
	minutes = minutes < 10 ? '0'+minutes : minutes;
	var strTime = hours + ':' + minutes + ' ' + ampm;
	return strTime;
}

async function get_bot_response(userMsg) {
    try {
        const response = await fetch('/bot-response', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({'msg':userMsg})
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
		console.log(result)

		


        return result;
    } catch (error) {
        console.error("Error:", error);
    }
}

function apply_bot_reply(botMsg) {
	const bot_response = `
		<div class="message-box others-message-box">
				<div class="message others-message">
					<div class="user-name">Bot <span>${formatAMPM(new Date)}</span></div>
					${botMsg}
				</div>
				<div class="separator"></div>
			</div>
		`

		document.getElementById("message-area").innerHTML+=bot_response;
			scrollToBottom()
}

function apply_user_reply(content){
	var html='<div class="message-box my-message-box">'+'<div class="message my-message">'+'<div class="user-name"><span>'+formatAMPM(new Date)+'</span> You</div>'+'<p>'+content.toString()+'</p></div>'+'<div class="separator"></div></div>';
	document.getElementById("typing-box").value="";
	document.getElementById("message-area").innerHTML+=html;
	scrollToBottom()
}

$('#typing-box').keyup( async function (event) {
	if (event.keyCode==13){
		var content=document.getElementById("typing-box").value;
		console.log(content)
		content=content.replace(/</g, "&lt;").replace(/>/g, "&gt;").trim()
		
		if (event.shiftKey){
		}else{
			apply_user_reply(content)
			const response = await get_bot_response(content)
			apply_bot_reply(response.bot_response)

		}
	}
})



document.addEventListener("DOMContentLoaded", () => {
    apply_bot_reply('Hello! How can I help you?')
});
