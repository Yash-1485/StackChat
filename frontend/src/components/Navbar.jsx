import { Link, useLocation } from "react-router";
import useAuthUser from "../hooks/useAuthUser";
import { BellIcon, HomeIcon, LogOutIcon, MessageSquareText, Users } from "lucide-react";
import ThemeSelector from "./ThemeSelector";
import useLogout from "../hooks/useLogout";

const Navbar = () => {
    const { authUser } = useAuthUser();
    const location = useLocation();
    const isChatPage = location.pathname?.startsWith("/chat");
    // const navigate=useNavigate();
    // const queryClient = useQueryClient();
    // const { mutate: logoutMutation } = useMutation({
    //   mutationFn: logout,
    //   onSuccess: () => queryClient.invalidateQueries({ queryKey: ["authUser"] }),
    // });

    const { logoutMutation } = useLogout();

    return (
        <nav className="bg-base-200 border-b border-base-300 sticky top-0 z-30 h-16 flex items-center">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className={`flex items-center ${isChatPage?"justify-between":"lg:justify-end justify-between"} w-full sm:gap-1 gap-[0.5px]`}>
                {/* LOGO - ONLY IN THE CHAT PAGE */}
                    {isChatPage && (
                        <div className="pl-3 sm:pl-5">
                            <Link to="/" className="flex items-center gap-2.5">
                                <MessageSquareText className="size-5 sm:size-9 text-primary" />
                                <span className="text-xl sm:text-3xl font-bold font-mono bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary  tracking-wider">
                                    StackChat
                                </span>
                            </Link>
                        </div>
                    )}

                    {
                        !isChatPage && (
                            <div className="lg:hidden pl-3 sm:pl-5">
                                <Link to="/" className="flex items-center gap-2.5">
                                    <MessageSquareText className="size-5 sm:size-9 text-primary" />
                                    <span className="text-xl sm:text-3xl font-bold font-mono bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary  tracking-wider">
                                        StackChat
                                    </span>
                                </Link>
                            </div>
                        )
                    }

                    <div className="flex justify-evenly">
                        <div className={`${isChatPage?"":"lg:hidden"} flex items-center gap-3 sm:gap-4`}>
                            <Link to={"/"}>
                                <button className="btn btn-ghost btn-circle">
                                    <HomeIcon className="w-5 h-5 sm:h-6 sm:w-6 text-base-content opacity-70" />
                                </button>
                            </Link>
                        </div>
                        
                        <div className={`${isChatPage?"":"lg:hidden"} flex items-center gap-3 sm:gap-4`}>
                            <Link to={"/friends"}>
                                <button className="btn btn-ghost btn-circle">
                                    <Users className="w-5 h-5 sm:h-6 sm:w-6 text-base-content opacity-70" />
                                </button>
                            </Link>
                        </div>

                        <div className="flex items-center gap-3 sm:gap-4">
                            <Link to={"/notifications"}>
                                <button className="btn btn-ghost btn-circle">
                                    <BellIcon className="w-5 h-5 sm:h-6 sm:w-6 text-base-content opacity-70" />
                                </button>
                            </Link>
                        </div>

                        {/* TODO */}
                        <ThemeSelector />

                        <div className="avatar">
                            {/* <div className="w-7 sm:w-9 rounded-full">
                                <img src={authUser?.profilePic} alt="User Avatar" rel="noreferrer" />
                            </div> */}
                            {/* <button type="button" className="btn btn-ghost btn-circle p-[0.5px]" onClick={()=>{navigate("/profile")}}>
                                <img src={authUser?.profilePic} alt="User Avatar" rel="noreferrer" />
                            </button> */}
                            <Link to={"/profile"}>
                                <button className="btn btn-ghost btn-circle p-[0.5px]">
                                    <img src={authUser?.profilePic} alt="User Avatar" rel="noreferrer" />
                                </button>
                            </Link>
                        </div>

                        {/* Logout button */}
                        <button className="btn btn-ghost btn-circle" onClick={logoutMutation}>
                            <LogOutIcon className="w-5 h-5 sm:h-6 sm:w-6 text-base-content opacity-70" />
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
};
export default Navbar;