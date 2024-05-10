import {useEffect} from "react";
import {BrowserRouter as Router, Route, Routes, useNavigate} from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import "./App.css";


    function App() {
        function RedirectToV0() {
            const navigate = useNavigate();

            useEffect(() => {
                navigate('/v0');
            }, [navigate]);

            return null;
        }

        return (
            <>
                <Router>
                    <Routes>
                        <Route path="/v0" element={<ChatPage version="v0"/>}/>
                        <Route path="/v1" element={<ChatPage version="v1"/>}/>
                        <Route path="/v2" element={<ChatPage version="v2"/>}/>
                        <Route path="*" element={<RedirectToV0/>}/>
                    </Routes>
                </Router>
            </>
        );
    }

    export default App;
