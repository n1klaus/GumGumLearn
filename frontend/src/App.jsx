// import logo from './logo.svg';
import './App.css';
import {Routes, Route, BrowserRouter} from 'react-router-dom';
import Login from './Login';
import Signup from './Signup';
import ResetPassword from './ResetPassword';
import Profile from './Profile';
import Home from './Home';
import { RequireToken} from './Components/Auth'
import Header from './Components/Header';
import Footer from './Components/Footer';

function App() {
  return (
    <div className ="App">
			<Header />
			<BrowserRouter>
				<Routes>
					<Route path="/" element = {<Home/>}/>
					<Route path="/login" element = {<Login/>}/>
					<Route path="/signup" element = {<Signup/>}/>
					<Route path="/forgot_password" element = {<ResetPassword/>}/>
					<Route path="/profile" element = {
						<RequireToken>
							<Profile/>
						</RequireToken>
						}
					/>
				</Routes>
			</BrowserRouter>
			<Footer />
		</div>
  );
}

export default App;
