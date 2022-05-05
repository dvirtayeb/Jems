import React from 'react'
import {Link} from 'react-router-dom';

function ThumbnailEmploye(props) {
    return (
        <div>
            <div className="btn-thumbnail">
                <Link to={props.link}>
            <div className="btn-image" >
            <img id="image1"src={props.image} alt="btn_image"/>
            </div>
            <div className="title">{props.title}</div>
            <div className="category">{props.category}</div>
        </Link>
        </div>
    </div>
    )
}

export default ThumbnailEmploye
