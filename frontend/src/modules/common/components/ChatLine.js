import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "../styles/ChatLine.css";

const ChatLine = ({ texto, rigth = false }) => {
    return (
        <div className={`${rigth ? "styled-box-right" : "styled-box-left"}`}>
            <div className="markdown-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {texto}
                </ReactMarkdown>
            </div>
        </div>
    );
};

export default ChatLine;

