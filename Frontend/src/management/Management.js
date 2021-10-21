// rfce shortcut
import React from 'react'  
import Thumbnail from './Thumbnail.js';
function Management() {
    return (
        <div>
            <Thumbnail
            link="/Management/Documents"
            image={"https://www.seekpng.com/png/detail/38-387179_document-file-folders-document-folder.png"}
            title="Documents"
            category=""            
            ></Thumbnail>
            <br/>
            <Thumbnail
            link="/Management/Employees"
            image={"https://www.seekpng.com/png/detail/124-1247481_engaged-vs-disengaged-employees.png"}
            title="Employees"
            category=""            
            ></Thumbnail>
        </div>
        
    )
}

export default Management

