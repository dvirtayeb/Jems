import './App.css';
// Pages
import SideBar from './SideBar';

// Style
import './static/css/App.css'
import './static/css/SideBar.css'
function App() {
  return (
    <div className="App">
      <meta name="viewport" content="width=device-width, initial-scale=1"></meta>
      <SideBar pageWrapId={'page-wrap'} outerContainerId={'outer-container'}/>
      <div className="App-header">
      </div>
    </div>
  );
}

export default App;
