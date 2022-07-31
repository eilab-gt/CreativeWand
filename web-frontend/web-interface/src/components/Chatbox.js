import React, {useEffect} from 'react';
import { Widget, addResponseMessage, toggleWidget, renderCustomComponent, toggleInputDisabled} from 'react-chat-widget';
import io from 'socket.io-client';
import './Chatbox.css'


import 'react-chat-widget/lib/styles.css';

// Note: chatbot widget documentation at https://github.com/Wolox/react-chat-widget/issues/130

const Chatbox = (props) => {

    useEffect(() => {
        addResponseMessage("Hello! I'm your Creative Wand.");
        toggleWidget();
        //toggleInputDisabled();
    }, []);

    useEffect(() => {
        const messageListener = (message) => {
            if (message['id'] === props.uuid) {
                addResponseMessage(message['message']);
            }
        };

        props.socket.on('message', messageListener);

        return () => {
          props.socket.off('message', messageListener);
        };
    }, [props.socket]);

    
    const handleNewUserMessage = async (newMessage) => {
        props.socket.emit('chat_message', {message: newMessage, code: props.code, id: props.uuid});
    };

    return (
        <div>
            <Widget
                handleNewUserMessage={handleNewUserMessage}
                resizable={true}
                title="Chat"
                subtitle="Talk to your Creative Wand here!"
            />
        </div>
    );
  }
  
export default Chatbox;
  