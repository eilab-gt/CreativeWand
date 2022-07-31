import React, {useEffect, useState} from 'react';
import Login from "./Login";
import {Link, Router} from "react-router-dom";
import {v4 as uuidv4} from 'uuid';


const Landing = (props) => {
    const [uuid, setUuid] = useState(uuidv4());

    const linkTarget = {
        pathname: "/?mode=2",
        key: uuidv4(), // we could use Math.random, but that's not guaranteed unique.
        state: {
            applied: true
        }
    };


    function linkWithMode(mode) {
        let myObject = {
            pathname: "/?mode=" + mode,
            key: uuidv4(), // we could use Math.random, but that's not guaranteed unique.
            state: {
                applied: true
            }
        }
        return myObject;


    }

    return (
        <div style={{marginBottom: 32}}>
            {/*<h2>===PILOT / DEBUG ===</h2>*/}
            <h2>Click "Help" at any time if you need to check instructions.</h2>
            <br/>
            <h2>In case you accidentally closed the survey window, just reopen it - Your progress is automatically
                saved.</h2>
            If things doesn't work, lemme know what is happening 😃
            <br/>
            Mode {props.mode}
        </div>
    );
}

export default Landing;