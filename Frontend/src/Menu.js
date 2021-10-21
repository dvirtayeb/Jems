import {Route, Switch } from 'react-router-dom'; 

import About from './About';
import CalculateTips from './CalculateTips';
import Login from './entry/Login';
import AddEmployee from './management/Employees/AddEmployee';
import DeleteEmployee from './management/Employees/DeleteEmployee';
import Documents from './management/Documents';
import Management from './management/Management';
import ShiftLogs from './ShiftsLog';
import Employees from './management/Employees';
import SignUp from './entry/SignUp';

function Menu(props) {
    return(
        <div className="menu">
            <Switch>
                <Route path="/CalculateTips" component={CalculateTips}/>
                <Route path="/ShiftsLog" component={ShiftLogs}/>
                <Route path="/About" component={About}/>
                <Route exact path="/Management" component={Management}/>
                <Route exact path="/Management/Employees" component={Employees}/>
                <Route exact path="/Management/Employees/AddEmployee" component={AddEmployee}/>
                <Route exact path="/Management/Employees/DeleteEmployee" component={DeleteEmployee}/>
                <Route exact path="/Management/Documents" component={Documents}/>
                <Route path="/Login" component={Login}/>
                <Route path="/SignUp" component={SignUp}/>
            </Switch>
        </div>
    )
}
export default Menu;