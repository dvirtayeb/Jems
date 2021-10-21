import React, {useState, useEffect} from 'react';
import './static/css/Calculate.css'
import WaiterRowTable from './WaiterRowTable';

function CalculateTips(){
    // # Shift (vars)
    const [error, setError] = useState("")
    const [date, setDateShift] = useState("")
    const [managers, setManager] = useState([""])
    const [selectedShift, setSelectedShift] = useState("")
    // # table Money (vars):
    const [totalHours] = useState("")
    const [totalCash, setTotalCash] = useState("")
    const [totalCredit, setTotalCredit] = useState("")
    const [cashPerHour] = useState("")
    const [creditPerHour] = useState("")
    const [totalTip] = useState("")
    //  # Table Waiters (vars):
    const [names, setNames] = useState(["", "", "", "","", "", "", "","", "", "", ""])
    const [startTime, setStartTime] = useState(["", "", "", "","", "", "", "","", "", "", ""])
    const [finishTime, setFinishTime] = useState(["", "", "", "","", "", "", "","", "", "", ""])
    const [totalWaiterTime, setTotalWaiterTime] = useState(["", "", "", "","", "", "", "","", "", "", ""])
    const [totalCashWaiter] = useState(["", "", "", "","", "", "", "","", "", "", ""])
    const [totalCreditWaiter] = useState(["", "", "", "","", "", "", "","", "", "", ""])
    const [totalTipWaiter] = useState(["", "", "", "","", "", "", "","", "", "", ""])

    const [data, setData] = useState({ "date": date , "managers": managers, "selected_shift": selectedShift, "total_hours": totalHours, 
        "total_cash": totalCash, "total_credit": totalCredit, "cash_per_hour": cashPerHour, "credit_per_hour": creditPerHour,
        "total_tip": totalTip, "names": names, "start_time": startTime, "finish_time": finishTime, "total_waiter_time": totalWaiterTime,
        "total_cash_waiter": totalCashWaiter, "total_credit_waiter": totalCreditWaiter, "total_tip_waiter": totalTipWaiter})

    const [submited, setSubmited] = useState(false)
    const [flag, setflag] = useState(true)
    useEffect(() => {
        if (flag){
            fetch('/CalculateTips',{
                headers: {'Content-Type': 'application/json; charest=UTF-8'},
            }).then(res => {
                if (!res.ok){
                    throw Error("could not fetch the data for that resource");
                }
                return res.json();
            })
            .then((data_res) => {
                setError(null);
                setflag(false)
                setData(data_res)
                setManager(data["managers"])
                console.log("Data(Get): ", data_res)
                

            }).catch(error => setError(error));
        }
        data["date"] = date
        data["manager"] = managers
        data["selected_shift"] = selectedShift
        data["total_cash"] = totalCash
        data["total_credit"] = totalCredit
        if (submited) {
            console.log("Data submited: ", data)
            fetch('/CalculateTips',{
                method: 'POST',
                headers: {'Content-Type': 'application/json; charest=UTF-8'},
                body: JSON.stringify(data),
            }).then(res => {
                console.log("RES:", res);
                if (!res.ok){
                    throw Error("could not fetch the data for that resource");
                }
                return res.json();
            })
            .then((data_res) => {
                console.log("Data_res('POST'):", data_res)
                setSubmited(false);
                setError(null);
                if (data_res.total_cash <= -1){
                    data["total_cash"] = -1
                    setTotalCash(-1)
                }
                if (data_res.total_credit <= -1 || data_res.total_credit === ""){
                    data["total_credit"] = -1
                    setTotalCredit(-1)
                }
                if (data["total_cash"] !== -1 && data["total_credit"] !== -1)
                    setData(data_res);
                console.log("Data: ", data)
                

            }).catch(error => setError(error));
        }
    }, [data, flag, submited,
        date, managers, selectedShift, totalCash, totalCredit, 
        names, totalWaiterTime, startTime, finishTime], []);
    
    function editName(i, value){
        data.names[i] = value;
        setNames();
    }
    function editStartTime(i, value){
        data.start_time[i] = value;
        setStartTime();
    }
    function editFinishTime(i, value){
        data.finish_time[i] = value;
        setFinishTime();
    }
    function editTime(i, value){
        data.total_waiter_time[i] = value;
        // console.log(data.total_waiter_time)
        setTotalWaiterTime(data.total_waiter_time[i]);
    }

    const chooseManager = (size) => {
        let managers = []
        for (let i =0 ; i < size ; i++){
            managers.push(
                <option 
                key={"managers"+i} 
                value={data["managers"][i]}
                id={"managers"+i}
                defaultValue="" 
                placeholder="Choose Manager">
                    {data["managers"][i]}
                </option>
            );
        }
        return managers

    }

    
    const handleSubmit = (event) => {
        event.preventDefault()
        setSubmited(true);
    }

    const createWaitersTable = (size) => {
        let waiters = [];
        for (let i =0 ; i < size ; i++){
            waiters.push(<WaiterRowTable key={"row"+i} names={data.names[i]}
            startTime={data.start_time[i]} finishTime={data.finish_time[i]}
            totalWaiterTime={data.total_waiter_time[i]}
            totalCashWaiter={data.total_cash_waiter} totalCreditWaiter={data.total_credit_waiter}
            totalTipWaiter={data.total_tip_waiter}
            editName={editName} editStartTime={editStartTime} editFinishTime={editFinishTime}
            editTime={editTime} i={i} screenPage="calculatePage"/>);
        }
        return waiters;
    };

    return(
        <div className="calculatetips">
            <br></br>
            {error && <div>{ error }</div>}
            <h1>Calculate tips</h1>
            <br></br>
            <form method="POST" onSubmit={handleSubmit}>
                <div className="bar_header">
                    <ul>
                        <li key="date">Date: <input name="date_shift" type="date" id="date_shift" value={date} onChange={event => setDateShift(event.target.value)}/></li>
                        <li key="managers">Managers:  
                            <select 
                            className="button_manager" 
                            name="managers" 
                            value={managers} 
                            onChange={event => setManager(event.target.value)}>
                                {chooseManager(2)}
                            </select>
                        </li>
                        <li key="selected_shift">Select Shift:  
                            <select className="button" name="shift" value={selectedShift} onChange={event => setSelectedShift(event.target.value)}>
                                <option value="morning"> משמרת בוקר </option>
                                <option value="evening">  משמרת ערב </option>
                            </select>
                        </li>
                    </ul>
                </div>
                <br/>
                <div className="table">
                    <table>
                        <tbody>
                            <tr key="money_inShift">
                                <td> </td>
                                <td><b> סה"כ שעות</b></td>
                                <td><b> סה"כ מזומן</b></td>
                                <td><b> סה"כ אשראי</b></td>
                                <td><b> מזומן לשעה  </b></td>
                                <td><b> אשראי לשעה  </b></td>
                                <td><b> סה"כ טיפ</b></td>
                            </tr>
                            <tr key="money2_inShift">
                                <td>#</td>
                                <td> {data.total_hours} </td>
                                <td><input type="float" id="Total-Cash" name="total_cash" placeholder="Total Cash" value={totalCash} onChange={event => setTotalCash(event.target.value)}/></td>
                                <td><input type="float" id="Total-Credit" name="total_credit" placeholder="Total Credit" value ={totalCredit} onChange={event => setTotalCredit(event.target.value)}/></td>
                                <td> {data.cash_per_hour} </td>
                                <td> {data.credit_per_hour} </td>
                                <td> {data.total_tip}</td>
                            </tr>
                        </tbody>
                    </table>

                    <br/>
                </div>
                <br/>

                <div>
                    <table id="waiters">
                        <tbody>
                            <tr key="waiter_inShift">
                                <td> </td>
                                <td><b> מלצר\ברמן: </b></td>
                                <td><b> שעת התחלה:  </b></td>
                                <td><b> שעת סיום:  </b></td>
                                <td><b> שעות:  </b></td>
                                <td><b> מזומן:  </b></td>
                                <td><b> אשראי:  </b></td>
                                <td><b> סה"כ:  </b></td>   
                            </tr>
                            {createWaitersTable(12)}
                        </tbody>
                    </table>
                </div>
            <br/>
            <h3><input className="submit" type="submit" name="Submit" value="Submit" /></h3>
            </form>
        </div>
    )
}
export default CalculateTips;
