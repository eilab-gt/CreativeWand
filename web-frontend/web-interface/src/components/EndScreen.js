import React, {useEffect} from 'react';
var md5 = require('md5');

const EndScreen = (props) => {

    const secret_code = md5(props.pid + props.pid)

    const code = props.code
    const pid = props.pid

    return (
        <div>
            <h3>Thanks for trying out Creative Wand!</h3>
            Your participant ID is: {pid}
            <br/>
            Your secret code is: "secret_{secret_code}"
        </div>
    );
}
  
export default EndScreen;
  