import Eimg from "./image/Eimg.png"
import Ebg from "./image/Ebg.png"
// import {BrowserRouter,Routes,Route} from "react-router-dom";
// import Elogin from "./Elogin.jsx"
// import ESignup from "./Esignup.jsx"
// import SST from "./SigntoText.jsx"
// import {Link} from "react-router-dom"

function Ehome(){

    return(
        <div className=" bg-[#6591FB] w-screen h-screen " >
            <div className="flex justify-around " >
                <div>
                    <div className="flex items-center pt-14 " >
                        <img src={Eimg} className="h-20 w-36 rounded-2xl rotate-[-27deg]  "/>
                        <p className="text-[#FFFDFD] text-[96px] font-semibold italic font-inter" >DITH</p>
                    </div>
                    <p className="text-[#FFFFFF] text-[36px] font-semibold italic font-inter" >Bridging the Communication<br/>Gap Between the Deaf and<br/>Hearing Communities</p>
                    <div className="flex  flex-col items-center gap-7 pt-20 " >
                        <button className="bg-[#4E61F6] h-12 w-24 rounded-lg hover:bg-[#061FE4] " >
                            <p className="text-[#FFFFFF] font-medium italic font-inter text-[20px] " >Sign Up</p>
                        </button>
                        <button className="bg-[#4E61F6] h-12 w-24 rounded-lg hover:bg-[#061FE4] " >
                            <p className="text-[#FFFFFF] font-medium italic font-inter text-[20px] " >Log In</p>
                        </button>
                    </div>
                </div>
                <div className=" flex justify-items-center w-[40%] pt-[3%] " >
                    <img src={Ebg} alt="background" className=" " />
                </div>
            </div>
        </div>
    );
}

export default Ehome