import React from 'react';
import './static/css/Calculate.css'


function WaiterRowTable({names, startTime, finishTime, totalWaiterTime, totalCashWaiter, 
    totalCreditWaiter, totalTipWaiter, editName, editStartTime, editFinishTime, editTime, i, screenPage}) {
        if(screenPage === "calculatePage"){
            return (<tr>
                <td>
                    {i + 1}
                </td>
                <td><input type="text" name={"name" + i} placeholder="Name" value={names}
                        onChange={event => editName(i, event.target.value)} />
                </td>
                <td>
                    <input type="time" name={"start_time" + i} placeholder="Start" value={startTime}
                        onChange={event => editStartTime(i, event.target.value)} />
                </td>
                <td>
                    <input type="time" name={"finish_time" + i} placeholder="Finish" value={finishTime}
                        onChange={event => editFinishTime(i, event.target.value)} />
                </td>
                <td>
                    <input type="float" name={"total_time" + i} placeholder="Time" value={totalWaiterTime}
                        onChange={event => editTime(i, event.target.value)} />
                </td>
                <td name={"total_cash_waiter"+i}>{totalCashWaiter[i]}</td>
                <td name={"total_credit_waiter"+i}>{totalCreditWaiter[i]}</td>
                <td name={"total_tip_waiter"+i}>{totalTipWaiter[i]}</td></tr>
            )
        }
        else{
            return (<tr>
                <td>{i + 1}</td>
                <td name={"name" + i}>{names}</td>
                <td name={"start_time" + i}>{startTime}</td>
                <td name={"finish_time" + i}>{finishTime}</td>
                <td name={"total_time" + i} >{totalWaiterTime}</td>
                <td name={"total_cash_waiter"+i}>{totalCashWaiter[i]}</td>
                <td name={"total_credit_waiter"+i}>{totalCreditWaiter[i]}</td>
                <td name={"total_tip_waiter"+i}>{totalTipWaiter[i]}</td>
                </tr>
                )
        }

} export default WaiterRowTable;