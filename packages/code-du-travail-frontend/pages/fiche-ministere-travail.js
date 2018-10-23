import React from "react";
import { withRouter } from "next/router";
import getConfig from "next/config";
import fetch from "isomorphic-unfetch";
import { ExternalLink } from "react-feather";
import Answer from "../src/search/Answer";

const {
  publicRuntimeConfig: { API_URL }
} = getConfig();

const fetchFiche = ({ slug }) =>
  fetch(`${API_URL}/items/fiches_ministere_travail/${slug}`).then(r =>
    r.json()
  );

const Source = ({ name, url }) => (
  <a href={url} target="_blank">
    Voir le contenu original sur : {name}{" "}
    <ExternalLink
      style={{ verticalAlign: "middle", margin: "0 5px" }}
      size={16}
    />
  </a>
);

class Fiche extends React.Component {
  static async getInitialProps({ res, query }) {
    return await fetchFiche(query)
      .then(data => ({
        data
      }))
      .catch(e => {
        console.log("e", e);
        res.statusCode = 404;
        throw e;
      });
  }

  render() {
    const { data } = this.props;
    const footer = (
      <Source name="Ministère du travail" url={data._source.url} />
    );
    return (
      <Answer
        title={data._source.title}
        emptyMessage="Cette fiche n'a pas été trouvée"
        html={data._source.html}
        footer={footer}
      />
    );
  }
}

export default withRouter(Fiche);
