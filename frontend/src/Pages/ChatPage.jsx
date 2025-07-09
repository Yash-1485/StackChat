import { useEffect, useState } from "react";
import { useParams } from "react-router";
import useAuthUser from "../hooks/useAuthUser";
import { useQuery } from "@tanstack/react-query";
import { getStreamToken } from "../lib/api";
import {Sun ,Moon} from "lucide-react";

import {
  Channel,
  ChannelHeader,
  Chat,
  MessageInput,
  MessageList,
  Thread,
  Window,
} from "stream-chat-react";
import { StreamChat } from "stream-chat";
import toast from "react-hot-toast";

import ChatLoader from "../components/ChatLoader";
import CallButton from "../components/CallButton";

import "stream-chat-react/dist/css/v2/index.css";

const STREAM_API_KEY = import.meta.env.VITE_STREAM_API_KEY;

import { useChatThemeStore, } from "../store/useThemeStore";

const ChatPage = () => {
    const { id: targetUserId } = useParams();

    const [chatClient, setChatClient] = useState(null);
    const [channel, setChannel] = useState(null);
    const [loading, setLoading] = useState(true);

    const { authUser } = useAuthUser();

    const { data: tokenData } = useQuery({
        queryKey: ["streamToken"],
        queryFn: getStreamToken,
        enabled: !!authUser, // this will run only when authUser is available
    });

    useEffect(() => {
        const initChat = async () => {
        if (!tokenData?.token || !authUser) return;
        try {
            console.log("Initializing stream chat client...");
            const client = StreamChat.getInstance(STREAM_API_KEY);
            await client.connectUser(
                {
                    id: String(authUser.id),
                    name: authUser.fullName,
                    image: authUser.profilePic,
                },
                tokenData.token
            );

            //
            const channelId = [String(authUser.id), targetUserId].sort().join("-");

            // you and me
            // if i start the chat => channelId: [myId, yourId]
            // if you start the chat => channelId: [yourId, myId]  => [myId,yourId]

            const currChannel = client.channel("messaging", channelId, {
                members: [String(authUser.id), targetUserId],
            });

            await currChannel.watch();

            setChatClient(client);
            setChannel(currChannel);
        } catch (error) {
            console.error("Error initializing chat:", error);
            toast.error("Could not connect to chat. Please try again.");
        } finally {
            setLoading(false);
        }
        };

        initChat();
    }, [tokenData, authUser, targetUserId]);

    const handleVideoCall = () => {
        if (channel) {
        const callUrl = `${window.location.origin}/call/${channel.id}`;

        channel.sendMessage({
            text: `I've started a video call. Join me here: ${callUrl}`,
        });

        toast.success("Video call link sent successfully!");
        }
    };

    const {chatTheme,setChatTheme}=useChatThemeStore();

    const toggleChatTheme=()=>{
        const newTheme = chatTheme === "light" ? "dark" : "light";
        setChatTheme(newTheme);
    }

    if (loading || !chatClient || !channel) return <ChatLoader />;

    return (
        <div className="h-[91.75vh] relative">
            <div className="themeToggleBtn absolute right-0 z-10 flex gap-2 p-2">
                <Sun className="text-yellow-600/90" />
                <div>
                    <input type="checkbox" className="toggle toggle-success bg-emerald-400 transition-all" name="themeToggle" id="themeToggle" onChange={()=>{toggleChatTheme()}} checked={chatTheme==="dark"} />
                </div>
                <Moon className="text-blue-800"/>
            </div>
            <Chat client={chatClient} theme={`messaging str-chat__theme-${chatTheme}`}>
                {/* Chat Theme Toggle Btn */}
                <Channel channel={channel}>
                <div className="w-full relative">
                    <CallButton handleVideoCall={handleVideoCall} />
                    <Window>
                        <ChannelHeader />
                        <MessageList />
                        <MessageInput focus />
                    </Window>
                </div>
                <Thread />
                </Channel>
            </Chat>
        </div>
    );
};
export default ChatPage;