import '../styles/App.css';
import {useDispatch} from "react-redux";
import {useEffect} from "react";
import Body from "./Body";
import Footer from "./Footer";
import Header from "./Header";

function App() {

  const dispatch = useDispatch();

  useEffect(() => {

  });

  return (
      <div className="app-container">
        <Header/>
        <Body></Body>
        <Footer/>
      </div>
  );
}

export default App;
