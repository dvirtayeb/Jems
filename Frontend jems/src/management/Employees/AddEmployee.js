import React from "react";

function AddEmployee(props){
    
    return(
        <div classname="addEmployee">
            <form method="POST" action="">
                <h1>Add/Edit New Employee</h1>
                <br/>
                <div classname="form_signup">
                    <div className="bar_header">
                        <li>Email: <input name="email" type="text" id="email" /></li>
                        <li>Name: <input name="name" type="text" id="email" /></li>
                        <li>Password: <input name="password" type="password" id="password" /></li>
                        <li>Re enter password: <input name="password2" type="password" id="password2" /></li>
                        <li>Age: <input name="age" type="text" id="age" /></li>
                        <li>Phone: <input name="phone" type="text" id="phone" /></li>
                        <li>Location: <input name="location" type="text" id="location" /></li>
                        <li>Role: <input name="role" type="text" id="role" /></li>
                        <li>Auth Password: <input name="auth" type="password" id="auth" /></li>
                    </div>
                <br/>
                <h3><input class="submit" type="submit" name="Submit" value="Submit"/></h3>
                </div>
            </form>
        </div>
    )
}
export default AddEmployee;