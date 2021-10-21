import {React, useState, useEffect} from "react";
import {Link, Redirect} from 'react-router-dom';
import { useForm } from 'react-hook-form';

function SignUp(props){
    var [submited, setSubmited] = useState(false)
    var [error, setError] = useState("")
    var [signUpForm] = useState({"email": "", "password": ""})
    const {register ,formState: {errors}} = useForm();
    var [msg, setMsg] = useState(false)

    const handleSubmit = (event) => {
        event.preventDefault()
        setSubmited(true);
        // if (msg) {
        //     return <Redirect to="/Login"/>
        // }
    }

    useEffect(() => {
        if (submited){
            // console.log("Data_submitted(Post): ", shift)
            fetch('/SignUp',{
                method: 'POST',
                headers: {'Content-Type': 'application/json; charest=UTF-8'},
                body: JSON.stringify(signUpForm),
            }).then(res => {
                if (!res.ok){
                    throw Error("could not fetch the data for that resource");
                }
                return res.json();
            })
            .then((data_result) => {
                console.log("Data_res: ", data_result);
                // setError(null);
                setSubmited(false)
                // setMsg(data_result["msg"]);


            }).catch(error => setError(error));
        }
    },[submited, signUpForm, msg]);

    return(
        <div className="signUp">
            <form method="POST" action={handleSubmit}>
                <h1>Create New Account</h1>
                <br/>
                <div className="form_signup">
                    <div className="bar_header">
                        {/* <li>UserName: <input {...register('userName')}/></li> */}
                        {/* <li>Email: <input {className="email" type="text" id="email}" /></li>
                        <li>Password: <input className="password" type="password" id="password" /></li>
                        <li>Re enter password: <input className="password2" type="password" id="password2" /></li>
                        <li>Auth Password: <input className="auth" type="password" id="auth" /></li> */}
                        <li>UserName: <input className="userName" type="text" id="userName" onChange={event => setName(event.tar)}/></li>
                        <li>Email: <input className="email" type="text" id="email" /></li>
                        <li>Password: <input className="password" type="password" id="password" /></li>
                        <li>Re enter password: <input className="password2" type="password" id="password2" /></li>
                        <li>Auth Password: <input className="auth" type="password" id="auth" /></li>
                    </div>
                <br/>
                <h3><input className="submit" type="submit" value="Submit"/></h3>
                <br/>
                <li >already have an account?
                    <Link to="/Login" className="signUp"> login </Link>
                instead.</li>
                </div>
            </form>
        </div>
    )
}
export default SignUp;