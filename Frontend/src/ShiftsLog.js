import {React, useState, useEffect} from "react";
import Shift from "./Shift";
function ShiftsLog(props){
    const [error, setError] = useState("")
    const [submited,setSubmited] = useState(false)
    const [detailsExist, setDetails] = useState(false)
    const [shift, setShift] = useState({"msg": "", "shift_exist": false, "shift": "","date": "", "managers": "", "selected_shift": "", "total_hours": "", 
    "total_cash": "", "total_credit": "", "cash_per_hour": "", "credit_per_hour": "",
    "total_tip": "", "names": [], "start_time": [], "finish_time": [], "total_waiter_time": [],
    "total_cash_waiter": [], "total_credit_waiter": [], "total_tip_waiter": []})
    useEffect(() => {
        if (submited){
            // console.log("Data_submitted(Post): ", shift)
            fetch('/ShiftsLog',{
                method: 'POST',
                headers: {'Content-Type': 'application/json; charest=UTF-8'},
                body: JSON.stringify(shift),
            }).then(res => {
                if (!res.ok){
                    throw Error("could not fetch the data for that resource");
                }
                return res.json();
            })
            .then((data_result) => {
                console.log("Data_res: ", data_result)
                setError(null);
                setSubmited(false)
                shift["shift_exist"] = data_result["shift_exist"]
                setShift(data_result)                

            }).catch(error => setError(error));
        }
    },[shift, submited, detailsExist]);

    const handleSubmit = (event) => {
        event.preventDefault()
        setSubmited(true);
    }

    // function showShift(shift_data) {
    //     // console.log("func: ", shift_data)
    //     if (shift["shift_exist"]){
    //         console.log("func, shift exist: ", shift_data)
    //         let shift_p = [];
    //         shift_p.push(<Shift key="shift0" report_details={shift["shift_exist"]} shift_details={shift_data}></Shift>)
    //         return shift_p;               
    //     }
    // }

    const showShift = (shift_data) => {
        // if (shift["shift_exist"]){
            return <Shift key ="shift0" report_details={shift["shift_exist"]} shift_details={shift_data}></Shift>
        // }
        // else {
        //     return (<div><br/><h3>Shift not found</h3></div>)
        // }
    }

    function editShift(shift_selected){
        shift["shift"] = shift_selected
        setDetails(shift["shift_exist"])
    }

    function editShowDate(dateShift){
        shift["date"] = dateShift
    }

    return(
        <div className="calculatetips">
            <h1>Shifts Log</h1>
            <form method="POST" onSubmit={handleSubmit}>
            <br/>
            <div className="bar_header">
                
                    <li key="date">Date: <input name="date_shift" type="date" id="date_shift" onChange={event => editShowDate(event.target.value)}/></li>
                    <br/>
                    <li key="selected_shift">Select Shift:  
                                <select className="button" name="shift" onChange={event => editShift(event.target.value)}>
                                    <option value="morning"> משמרת בוקר </option>
                                    <option value="evening">  משמרת ערב </option>
                                </select>
                            </li>
            </div>
            <br/>
            <h3><input className="submit" type="submit" name="Submit" value="Search"/></h3>
            {showShift(shift)}
            </form>
        </div>
    )
}
export default ShiftsLog;