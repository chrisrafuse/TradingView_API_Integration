//This is Nav Bar Component

import { Link } from "react-router-dom";

function Nav() {
  return (
    <div className="flex justify-center">
    <nav className="w-[50%] p-4 bg-gray-200 flex justify-center  shadow-md rounded-[10%]">
      <Link className="mr-4" to="/">
        Home
      </Link>
      <Link className="mr-4" to="/orders">
        Orders
      </Link>
      <Link className="mr-4" to="/positions">
        Positions
      </Link>
      <Link to="/webhooks">Webhooks</Link>
    </nav>
    </div>
  );
}
export default Nav;
