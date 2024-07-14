import React from "react";

function Loader({width, height}) {
    return (
        <div style={{textAlign:'center'}}>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width={width || "60"}
                height={height || "60"}
                ariaBusy="true"
                ariaLabel="dna-loading"
                className="dna-wrapper"
                color="#000"
                data-testid="dna-svg"
                preserveAspectRatio="xMidYMid"
                viewBox="0 0 100 100"
            >
                <circle
                    cx="6.452"
                    cy="60.623"
                    r="3.42"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-0.5s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="0s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-0.5s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="6.452" cy="39.377" r="2.58" fill="black">
                    <animate
                        attributeName="r"
                        begin="-1.5s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-0.5s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
                <circle
                    cx="16.129"
                    cy="68.155"
                    r="3.18"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-0.7s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-0.2s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-0.7s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="16.129" cy="31.845" r="2.82" fill="black">
                    <animate
                        attributeName="r"
                        begin="-1.7s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1.2s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-0.7s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
                <circle
                    cx="25.806"
                    cy="69.363"
                    r="2.94"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-0.9s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-0.4s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-0.9s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="25.806" cy="30.637" r="3.06" fill="black">
                    <animate
                        attributeName="r"
                        begin="-1.9s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1.4s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-0.9s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
                <circle
                    cx="35.484"
                    cy="65.367"
                    r="2.7"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-1.1s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-0.6s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.1s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="35.484" cy="34.633" r="3.3" fill="black">
                    <animate
                        attributeName="r"
                        begin="-2.1s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1.6s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.1s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
                <circle
                    cx="45.161"
                    cy="53.847"
                    r="2.46"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-1.3s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-0.8s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.3s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="45.161" cy="46.153" r="3.54" fill="black">
                    <animate
                        attributeName="r"
                        begin="-2.3s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1.8s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.3s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
                <circle
                    cx="54.839"
                    cy="39.377"
                    r="2.58"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-1.5s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.5s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="54.839" cy="60.623" r="3.42" fill="black">
                    <animate
                        attributeName="r"
                        begin="-2.5s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-2s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.5s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
                <circle
                    cx="64.516"
                    cy="31.845"
                    r="2.82"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-1.7s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1.2s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.7s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="64.516" cy="68.155" r="3.18" fill="black">
                    <animate
                        attributeName="r"
                        begin="-2.7s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-2.2s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.7s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
                <circle
                    cx="74.194"
                    cy="30.637"
                    r="3.06"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-1.9s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1.4s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.9s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="74.194" cy="69.363" r="2.94" fill="black">
                    <animate
                        attributeName="r"
                        begin="-2.9s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-2.4s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-1.9s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
                <circle
                    cx="83.871"
                    cy="34.633"
                    r="3.3"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-2.1s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1.6s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-2.1s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="83.871" cy="65.367" r="2.7" fill="black">
                    <animate
                        attributeName="r"
                        begin="-3.1s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-2.6s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-2.1s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
                <circle
                    cx="93.548"
                    cy="46.153"
                    r="3.54"
                    fill="rgba(233, 12, 89, 0.5125806451612902)"
                >
                    <animate
                        attributeName="r"
                        begin="-2.3s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-1.8s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-2.3s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="rgba(233, 12, 89, 0.5125806451612902);#ff0033;rgba(233, 12, 89, 0.5125806451612902)"
                    ></animate>
                </circle>
                <circle cx="93.548" cy="53.847" r="2.46" fill="black">
                    <animate
                        attributeName="r"
                        begin="-3.3s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="2.4000000000000004;3.5999999999999996;2.4000000000000004"
                    ></animate>
                    <animate
                        attributeName="cy"
                        begin="-2.8s"
                        calcMode="spline"
                        dur="2s"
                        keySplines="0.5 0 0.5 1;0.5 0 0.5 1"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="30.5;69.5;30.5"
                    ></animate>
                    <animate
                        attributeName="fill"
                        begin="-2.3s"
                        dur="2s"
                        keyTimes="0;0.5;1"
                        repeatCount="indefinite"
                        values="black;rgba(53, 58, 57, 0.1435483870967742);black"
                    ></animate>
                </circle>
            </svg>
        </div>
    );
}

export default Loader;