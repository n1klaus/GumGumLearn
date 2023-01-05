import { useNavigate } from "react-router"
import Button from 'react-bootstrap/Button';

export default function Profile(){

	const navigate = useNavigate();

	const signOut = ()=> {
		localStorage.removeItem('token')
		navigate('/')
	}
	return(
		<>
			<div style ={{marginTop:20,minHeight:700}}>
				<h1>Profile page</h1>
				<p>Hello there, welcome to your profile page</p>

				<Button onClick = {signOut}>sign out</Button>
			</div>
		</>
	)
}
