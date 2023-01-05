import { useNavigate } from "react-router"
import SearchBar from './Components/SearchBar';

export default function Home() {
	const navigate = useNavigate();
	return (
		<div className="container" style={{ marginInlineStart: 450, marginTop: 300 }} 
		onClick={navigate("/")}>
			<SearchBar/>
		</div>
	)
}
