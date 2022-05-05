import {React, useState, useEffect} from "react";
import {Link, Redirect} from 'react-router-dom';
function Login(props){
    var [submited, setSubmited] = useState(false)
    var [error, setError] = useState("")
    var [loginForm] = useState({"email": "", "password": ""})
    var [msg, setMsg] = useState(false)

    const handleSubmit = (event) => {
        event.preventDefault()
        setSubmited(true);
        if (msg) {
            return <Redirect to="/"/>
        }
    }

    useEffect(() => {
        if (submited){
            // console.log("Data_submitted(Post): ", shift)
            fetch('/Login',{
                method: 'POST',
                headers: {'Content-Type': 'application/json; charest=UTF-8'},
                body: JSON.stringify(loginForm),
            }).then(res => {
                if (!res.ok){
                    throw Error("could not fetch the data for that resource");
                }
                return res.json();
            })
            .then((data_result) => {
                console.log("Data_res: ", data_result);
                setError(null);
                setSubmited(false)
                setMsg(data_result["msg"]);


            }).catch(error => setError(error));
        }
    },[submited, loginForm, msg]);
    return(
        <div classname="login">
            <form method="POST" action={handleSubmit}>
                <h2>Login to system:</h2>
                <br/>
                <div classname="form_signup">
                    <div className='box'>
                        <div className="bar_header">
                            <li>Email: <input name="email" type="text" id="email" /></li>
                            <li>Password: <input name="password" type="password" id="password" /></li>
                        </div>
                    </div>
                <br/>
                <h3><input class="submit" type="submit" name="Submit" value="Login"/></h3>
                <br/>
                <li ><strong>Need to register? </strong><Link to="/SignUp" className="signUp">
                    Create New Account
                    </Link></li>
                </div>
            </form>
        </div>
    )
}
export default Login;