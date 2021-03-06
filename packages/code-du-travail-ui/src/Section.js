import React from "react";
import PropTypes from "prop-types";

const Section = ({ light, dark, style, children }) => {
  const containerClassName = light
    ? "section-light"
    : dark
      ? "section-dark"
      : "section";
  const innerContainerClassName = light
    ? "wrapper-light"
    : dark
      ? "wrapper-dark"
      : "wrapper";
  return (
    <div className={containerClassName} style={style}>
      <div className="container">
        <div className={innerContainerClassName}>{children}</div>
      </div>
    </div>
  );
};

Section.propTypes = {
  children: PropTypes.element.isRequired,
  style: PropTypes.object,
  light: PropTypes.bool,
  dark: PropTypes.bool
};

Section.defaultProps = {
  light: false,
  dark: false
};

export default Section;
