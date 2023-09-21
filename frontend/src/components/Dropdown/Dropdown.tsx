import { useState, useEffect, useRef, ReactNode } from "react";
import { AiOutlineHolder } from "react-icons/ai";
import { BiCheck } from "react-icons/bi";
import "./dropdown.css";

/**
 * Props for the Dropdown component.
 */
export interface DropdownProps {
  /** Label for the dropdown */
  dropDownLabel?: string;
  /** Options for the dropdown */
  options: string[];
  /** Currently selected option */
  selectedOption: string;
  /** Function to set the selected option */
  setSelectedOption: (option: string) => void;
  /** Alignment for the dropdown */
  align?: "left" | "right";
  /** Children to display as the dropdown's trigger */
  children: ReactNode;
}

/**
 * A dropdown component for selecting an option from a list.
 */
export default function Dropdown({
  dropDownLabel,
  options,
  selectedOption,
  setSelectedOption,
  align,
  children,
}: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);

  const filterRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (
        filterRef.current &&
        !filterRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);

  return (
    <div className="dropdown noselect" ref={filterRef}>
      <div className="toggle" onClick={() => setIsOpen(!isOpen)}>
        {children}
      </div>
      <div
        data-align={align || "right"}
        data-visible={isOpen}
        className="dropdown-content"
      >
        {dropDownLabel && <h1>{dropDownLabel}</h1>}
        {options?.map((option: string, index: number) => (
          <div
            className="option"
            key={index}
            onClick={() => setSelectedOption(option)}
          >
            <div className="content">
              {typeof option === "boolean"
                ? option
                  ? "Yes"
                  : "No"
                : String(option)}
            </div>
            <div className="check">
              {selectedOption === option && <BiCheck />}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
