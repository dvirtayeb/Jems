import {React, Component } from 'react';
import {elastic as Menu } from 'react-burger-menu';
import {Link} from 'react-router-dom';
import MenuPage from './Menu';
import './static/css/SideBar.css'

class SideBar extends Component {
  constructor(props){
    super(props)
    this.state = {
      sidebar: false
    }
  }
  
  handleStateChange(state) {
    this.setState({sidebar: state.isOpen});
  }
  closeSidebar () {
    this.setState({sidebar: false});
  }
  toggleSidebar() {
    this.setState(state => ({sidebar: !state.sidebar}));
  }
  
  render() {
    return(
        <div className="navigation">
          <div className="navigation-sub">
            <div className="nav_item">
            <Link to="/" className="item">Home </Link>
            <Link to="/Management" className="item">Management </Link> {/* Visible only for managers 
            , create Factory Objects: managers, sub-Manager, waiters, barthender*/}
            {/* create for management employees :add, delete ,change */}
            <Link to="/Login" className="item">Login </Link>
            </div>
            <br></br>
            <MenuPage id ="page"></MenuPage>
            <Menu isOpen={this.state.sidebar} onStateChange={(state) => this.handleStateChange(state)}>
                  <li ><Link to="/CalculateTips" className="bm-item" onClick={() => this.closeSidebar()}>
                  Calculate Tips
                    </Link></li>
                  <li ><Link to="/ShiftsLog" className="bm-item" onClick={() => this.closeSidebar()}>
                  Shifts - Log
                    </Link></li>
                  <li ><Link to="/About" className="bm-item" onClick={() => this.closeSidebar()}>
                    About 
                    </Link></li>
            </Menu>
          </div>
        </div>
    )
  }
}

export default SideBar;