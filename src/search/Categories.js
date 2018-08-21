import React from "react";
import Router from "next/router";

class Categories extends React.Component {
  handleClick = (event, query) => {
    event.preventDefault();
    this.props.urlUpdate(encodeURI(query));
  };

  render() {
    return (
      <section className="section-light">
        <div className="container">
          <div className="categories">
            <header className="center">
              <h2 className="no-margin">Retrouvez nos réponses thématiques</h2>
            </header>
            <ul className="categories__list">
              <li className="categories__list-item">
                <a
                  href="#"
                  onClick={e => this.handleClick(e, "embauche et contrat")}
                >
                  <img src="/static/assets/icons/handshake.svg" alt="" />
                  <h3>Embauche et contrat</h3>
                </a>
              </li>
              <li className="categories__list-item">
                <a
                  href="#"
                  onClick={e =>
                    this.handleClick(e, "durée de travail et congés")
                  }
                >
                  <img src="/static/assets/icons/time.svg" alt="" />
                  <h3>Durée de travail et congés</h3>
                </a>
              </li>
              <li className="categories__list-item">
                <a href="#" onClick={e => this.handleClick(e, "rémunération")}>
                  <img src="/static/assets/icons/coins.svg" alt="" />
                  <h3>Rémunération</h3>
                </a>
              </li>
              <li className="categories__list-item">
                <a
                  href="#"
                  onClick={e => this.handleClick(e, "santé et sécurité")}
                >
                  <img src="/static/assets/icons/shield.svg" alt="" />
                  <h3>Santé et sécurité</h3>
                </a>
              </li>
              <li className="categories__list-item">
                <a
                  href="#"
                  onClick={e => this.handleClick(e, "rupture de contrat")}
                >
                  <img src="/static/assets/icons/file-3.svg" alt="" />
                  <h3>Rupture de contrat</h3>
                </a>
              </li>
              <li className="categories__list-item">
                <a href="#" onClick={e => this.handleClick(e, "formation")}>
                  <img src="/static/assets/icons/hiring-1.svg" alt="" />
                  <h3>Formation</h3>
                </a>
              </li>
              <li className="categories__list-item">
                <a
                  href="#"
                  onClick={e => this.handleClick(e, "dialogue social")}
                >
                  <img src="/static/assets/icons/chat.svg" alt="" />
                  <h3>Dialogue social</h3>
                </a>
              </li>
              <li className="categories__list-item">
                <a
                  href="#"
                  onClick={e => this.handleClick(e, "maladies et inaptitudes")}
                >
                  <img src="/static/assets/icons/certificate.svg" alt="" />
                  <h3>Maladies et inaptitudes</h3>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </section>
    );
  }
}

export default Categories;