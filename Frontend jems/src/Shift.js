import React from 'react'
import WaiterRowTable from './WaiterRowTable'

function Shift(data) {
    const showWaiters = (shiftData) =>{
        let waiters = [];
        if(data["report_details"] === true){
            for (let i =0 ; i < 12 ; i++){
                waiters.push(<WaiterRowTable key={"row"+i} names={data["shift_details"].names[i]}
                startTime={data["shift_details"].start_time[i]} finishTime={data["shift_details"].finish_time[i]}
                totalWaiterTime={data["shift_details"].total_waiter_time[i]}
                totalCashWaiter={data["shift_details"].total_cash_waiter} totalCreditWaiter={data["shift_details"].total_credit_waiter}
                totalTipWaiter={data["shift_details"].total_tip_waiter} i={i} screenPage="showPage"/>)
            }
        }
        return waiters
    } 
    if (data["shift_details"].shift_exist === false) {
        return(<div id="displayShift0"></div> )
    }
    else if (data["shift_details"].shift_exist === true) {
        return (
            <div>            
                <div id="displayShift1">
                    
                    <br/>
                    <h1> Shift: {data["shift_details"].date} </h1>
                    <ul>
                        <div className='box'>
                            <li><strong>Manager:</strong>   {data["shift_details"].managers}</li>
                            <li><strong>Shift:</strong>   {data["shift_details"].selected_shift}</li>
                        </div>
                    </ul>
                    <br/>
                    <table>
                        <tbody>
                            <tr>
                                <td> </td>
                                <td><b> סה"כ שעות</b></td>
                                <td><b> סה"כ מזומן</b></td>
                                <td><b> סה"כ אשראי</b></td>
                                <td><b> מזומן לשעה  </b></td>
                                <td><b> אשראי לשעה  </b></td>
                                <td><b> סה"כ טיפ</b></td>
                            </tr>
                            <tr>
                                <td>#</td>
                                <td> {data["shift_details"].total_hours} </td>
                                <td> {data["shift_details"].total_cash} </td>
                                <td> {data["shift_details"].total_credit} </td>
                                <td> {data["shift_details"].cash_per_hour} </td>
                                <td> {data["shift_details"].credit_per_hour} </td>
                                <td> {data["shift_details"].total_tip}</td>
                            </tr>
                            <tr>
                                <td> </td>
                                <td><b> מלצר\ברמן: </b></td>
                                <td><b> שעת התחלה:  </b></td>
                                <td><b> שעת סיום:  </b></td>
                                <td><b> שעות:  </b></td>
                                <td><b> מזומן:  </b></td>
                                <td><b> אשראי:  </b></td>
                                <td><b> סה"כ:  </b> </td>
                            </tr>
                        </tbody>
                        <tbody>
                            {showWaiters(data["shift_details"])}
                        </tbody>
                    </table>
                    <br/>
                </div>           
            </div>
        )
        }
        else{
            return <div><br/><h3>Shift not found</h3></div>
        }
}export default Shift
