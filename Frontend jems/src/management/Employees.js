import React from 'react'
import ThumbnailEmploye from './Employees/ThumbnailEmploye';

function Employees() {
    return (
        <div>
            <ThumbnailEmploye
            link="/Management/Employees/AddEmployee"
            image={"https://www.seekpng.com/png/detail/44-444040_add-user-group-woman-man-icon-add-group.png"}
            title="Add/Edit Employee"
            category=""            
            ></ThumbnailEmploye>
            <br/>
            <ThumbnailEmploye
            link="/Management/Employees/DeleteEmployee"
            image={"https://www.seekpng.com/png/detail/202-2022743_edit-delete-icon-png-download-delete-icon-png.png"}
            title="Delete Employee"
            category=""            
            ></ThumbnailEmploye>
        </div>
    )
}

export default Employees;
