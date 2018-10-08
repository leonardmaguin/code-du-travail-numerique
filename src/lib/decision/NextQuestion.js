import { filterDocs, getNextQuestion } from "./walker";

// todo: themes

// arrange results tags format for the decision tree
// input : ["branche:hotellerie", "branche:restauration"]
// output : {branche:["hotellerie", "restauration"],tag2:[...],tag3:[...]}
const fixDocsTags = hits =>
  hits.map(hit => ({
    ...hit._source,
    tags:
      hit._source.tags &&
      hit._source.tags.reduce(
        (tags, cur) => {
          const [tag, value] = cur.split(":");
          if (!tags[tag]) {
            tags[tag] = [];
          }
          tags[tag].push(value);
          return tags;
        },
        {
          source: hit._source.source
        }
      )
  }));

// just wrap the walker API
const NextQuestion = ({ data, filters, render }) => {
  const results = filterDocs({ docs: fixDocsTags(data), filters });
  // get best guess
  let question =
    results.length > 1 &&
    getNextQuestion({
      docs: results,
      filters,
      // list of tag to use
      tags: [
        "branche",
        "profil",
        "theme",
        "contrat",
        "region",
        "sousTheme",
        "type_entreprise"
      ]
    });
  return render({ question, results });
};

export default NextQuestion;
