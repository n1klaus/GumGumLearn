// import logo from './logo.svg';
import "./App.css";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "react-query";
import Login from "./Login";
import Signup from "./Signup";
import ResetPassword from "./ResetPassword";
import Profile from "./Profile";
import Home from "./Home";
import About from "./About";
import Contact from "./Contact";
import { RequireToken } from "./Components/Auth";
import Header from "./Components/Header";
import Footer from "./Components/Footer";

const queryClient = new QueryClient();

function App() {
  return (
    <div className="App-container">
      <QueryClientProvider client={queryClient}>
        <Header />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/forgot_password" element={<ResetPassword />} />
            <Route
              path="/profile"
              element={
                <RequireToken>
                  <Profile />
                </RequireToken>
              }
            />
          </Routes>
        </BrowserRouter>
        <Footer />
      </QueryClientProvider>
    </div>
  );
}

export default App;
