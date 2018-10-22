import React from "react";
import PropTypes from "prop-types";

class DateContenu extends React.Component {
  static propTypes = {
    value: PropTypes.string
  };

  render() {
    return (
      <div className="article__date">Publié le&nbsp;: {this.props.value}</div>
    );
  }
}

export { DateContenu };
