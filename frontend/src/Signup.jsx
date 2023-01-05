import { useNavigate } from "react-router"
import { fetchToken, setToken } from "./Components/Auth"
import { useState } from "react"
import axios from "axios"
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function Signup(){
	const navigate = useNavigate()
	const [username,setUsername] = useState('')
	const [password,setPassword] = useState('')
	const [repeat_password,setRepeatPassword] = useState('')

	//check to see if the fields are not empty
	const signup = () => {

		if(username === '' & password === '' & repeat_password === ''){
			return
		}else{
			if (password !== repeat_password) {
				return
			}
			// make api call to our backend. we'll leave thisfor later
			axios.post('http://localhost:8000/signup',{
				username: username,
				password: password,
				repeat_password: repeat_password
			})
			.then(function(response){
				console.log(response.data.token,'response.data.token')
				if(response.data.token){
					setToken(response.data.token)
					navigate("/");
				}
			})
			.catch(function(error){
				alert("Signup failed");
				console.error(error,'error');
			});
		}
	}
	return(
		<div style={{minHeight:800, marginTop:30}}>
			<h1>Signup page</h1>
			<div style={{marginTop:30}}>
				{
					fetchToken() ? (
						<p>You are logged in</p>
					) : ( 
						<div>
							<Form>
								<Form.Group as={Row} className="mb-3" controlId="formBasicUsername">
									<Form.Label column sm="2">
										Username
									</Form.Label>
									<Col sm="3">
										<Form.Control type="text" placeholder="Enter username" onChange={(e)=>setUsername(e.target.value)} required/>
										<Form.Text className="text-muted">
											This cannot be changed in the future.
										</Form.Text>
									</Col>
								</Form.Group>

								<Form.Group as={Row} className="mb-3 align-content-sm-center" controlId="formBasicPassword">
									<Form.Label column sm="2">
										Password
									</Form.Label>
									<Col sm="3">
										<Form.Control className="input-control" type="password" placeholder="Password" onChange={(e)=>setPassword(e.target.value)} required/>
									</Col>
								</Form.Group>

								<Form.Group as={Row} className="mb-3 align-content-sm-center" controlId="formBasicPassword">
									<Form.Label column sm="2">
										Repeat Password
									</Form.Label>
									<Col sm="3">
										<Form.Control className="input-control" type="password" placeholder="Password" onChange={(e)=>setRepeatPassword(e.target.value)} required/>
									</Col>
								</Form.Group>
								{/* <Form.Group as={Row} className="mb-3 ml-5" controlId="formBasicCheckbox">
									<Col sm="2">
										<Form.Check type="checkbox" label="Agree to terms and conditions" />
									</Col>
								</Form.Group> */}
								<Col sm="6">
									<Button variant="primary" type="submit" onClick={signup}>
										Sign up
									</Button>
									<br></br>
									<a href="/login">Log in</a>
								</Col>
							</Form>
						</div>
					)
				}
			</div>
		</div>	
	)
}
