import { useState, useEffect } from "react";
import Lottie from "lottie-react";
import { IoReloadOutline, IoChevronDown } from "react-icons/io5";
import { SiBlockchaindotcom } from "react-icons/si";

import Dropdown from "../../components/Dropdown/Dropdown";
import APIService from "../../api/Service";

import { datasets, models } from "../../data";
import { Log } from "../../models/logs";
import LearningRobot from "../../assets/learning-robot.json";
import Processing from "../../assets/procecssing.json"
import Success from "../../assets/success.json"
import "./parachain.css";

export default function ParaChain() {
  const [logs, setLogs] = useState<Log[]>([]);
  const [selectedDataset, setSelectedDataset] = useState(datasets[0].label);
  const [selectedModel, setSelectedModel] = useState(models[0]);
  const [scores, setScores] = useState<{ before: number; after: number }>();

  const [state, setState] = useState("initial");
  // states are initial, waiting, completed

  const updateLogs = () => {
    APIService.GetData("blocks").then((data) => {
      setLogs(data.blocks);
    });
  };

  const initiateTraining = () => {
    setState("waiting");
    APIService.PostData("localupdate", {
      dataset: datasets.find((d) => d.label === selectedDataset)?.value,
    }).then((newScores) => {
      setState("completed");
      setTimeout(() => setState("initial"), 8000);
      setScores(newScores);
    });
  };

  const initiateMining = () => {
    setState("waiting");
    APIService.GetData("mine").then((data) => {
      // console.log(data);
      setState("completed");
      setTimeout(() => setState("initial"), 8000);
    });
  };

  useEffect(() => {
    updateLogs();
  }, []);

  return (
    <div className="page-container">
      <div className="left">
        <span className="toolbox">
          <div className="reload-button" onClick={updateLogs}>
            <IoReloadOutline />
          </div>
        </span>
        <div className="logs-wrapper">
          {logs.map((log: Log, index: number) => (
            <div className="log-container noselect" key={index}>
              <div className="header">
                <div className="left">
                  <div className="logo">
                    <SiBlockchaindotcom />
                  </div>
                  <div className="content">
                    <h4>Block</h4>
                    <p>Block Number {index + 1}</p>
                  </div>
                </div>
                <p className="timestamp">
                  {new Date(log.timestamp * 1000).toString()}
                </p>
              </div>
              <span>
                <h4>Current Hash</h4>
                <p>{log.hash}</p>
              </span>
              <span>
                <h4>Previous Hash</h4>
                <p>{log.previous_hash}</p>
              </span>
            </div>
          ))}
        </div>
      </div>
      <div className="right">
        <div className="animated-image">
          {state === "initial" && <Lottie animationData={LearningRobot} loop={true} />}
          {state === "waiting" && <Lottie animationData={Processing} loop={true} />}
          {state === "completed" && <Lottie animationData={Success} loop={true} />}
        </div>
        <h1>
          {state === "initial" && "Start Training"}
          {state === "waiting" && "Training In-Progress"}
          {state === "completed" && "Training Completed"}
        </h1>
        <div className="row">
          <div className="col">
            <p>Select Model</p>
            <Dropdown
              options={models}
              selectedOption={selectedModel}
              setSelectedOption={setSelectedModel}
              align="left"
            >
              <div className="selector">
                <p>{selectedModel}</p>
                <IoChevronDown />
              </div>
            </Dropdown>
          </div>
          <div className="col">
            <p>Select Dataset</p>
            <Dropdown
              options={datasets.map((i) => i.label)}
              selectedOption={selectedDataset}
              setSelectedOption={setSelectedDataset}
              align="left"
            >
              <div className="selector">
                <p>{selectedDataset}</p>
                <IoChevronDown />
              </div>
            </Dropdown>
          </div>
        </div>
        {scores && (
          <div className="row">
            <div className="col">
              <p>Accuracy Before</p>
              <span className="selector">{scores.before}</span>
            </div>
            <div className="col">
              <p>Accuracy After</p>
              <span className="selector">{scores.after}</span>
            </div>
          </div>
        )}
        <div className="btns-wrapper">
          <button
            className="training-btn"
            onClick={initiateTraining}
            disabled={state !== "initial"}
          >
            Initiate Training
          </button>
          <button
            className="mine-btn"
            onClick={initiateMining}
            disabled={state !== "initial"}
          >
            Mine
          </button>
        </div>
      </div>
    </div>
  );
}
