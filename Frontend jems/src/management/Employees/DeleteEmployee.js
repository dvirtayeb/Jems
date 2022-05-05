import React from "react";

function DeleteEmployee(props){
    
    return(
        <div classname="deleteEmployee">
            <form method="POST" action="">
                <h1>Delete Employee</h1>
                <br/>
                <div classname="form_signup">
                    <div className="bar_header">
                        <li>Email: <input name="email" type="text" id="email" /></li>
                        <li>Name: <input name="name" type="text" id="email" /></li>
                        <li>Auth Password: <input name="auth" type="password" id="auth" /></li>
                    </div>
                <br/>
                <h3><input class="submit" type="submit" name="Submit" value="Submit"/></h3>
                </div>
            </form>
        </div>
    )
}
export default DeleteEmployee;