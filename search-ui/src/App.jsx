import React from "react";
import {
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  Paging,
  WithSearch,
  Facet,
} from "@elastic/react-search-ui";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import "./App.css"

const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200", // for local
  index: "cv-transcriptions",
});

const config = {
  searchQuery: {
    search_fields: {
      generated_text: { weight : 3},
      // filename: {},
    },
    result_fields: {
      // filename: { raw: {}},
      generated_text: { raw: {} },
      duration: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} },
    },
     facets: {
      age: { type: 'value' },
      gender: { type: 'value' },
      accent: { type: 'value' },
      duration: {
        type: 'range',
        ranges: [
          { from: 0, to: 2, name: '2s' },
          { from: 2, to: 4, name: '4s' },
          { from: 4, to: 6, name: '6s' },
          { from: 6, to: 8, name: '8s' },
          { from: 8, to: 10, name: '10s' },
          { from: 10, to: 12, name: '12s' },
          { from: 12, to: 14, name: '14s' },
          { from: 14, name: 'Long' }
        ]
      }
    },
  },
  alwaysSearchOnInitialLoad: true,
  apiConnector: connector,
};


const CustomResultView = ({ result }) => (
  <div className="sui-result">
    <div className="sui-result-row">
      <div>
        <strong>Generated Text</strong>
      </div>
      <div className="sui-result-value">
        {result.generated_text.raw}
      </div> 
    </div>
    <div className="sui-result-row">
      <div>
        <strong>Age</strong>
      </div>
      <div className="sui-result-value">
        {result.age.raw}
      </div>
    </div>
    <div className="sui-result-row">
      <div>
        <strong>Gender</strong>
      </div> 
      <div className="sui-result-value">
        {result.gender.raw}
      </div>  
    </div>
    <div className="sui-result-row">
      <div>
        <strong>Accent</strong>
      </div>  
      <div className="sui-result-value">
        {result.accent.raw}
      </div>
      </div>
    <div className="sui-result-row">
      <div>
        <strong>Duration</strong>
      </div>
      <div className="sui-result-value">  
        {result.duration.raw}
      </div>  
    </div>
  </div>
);

export default function App() {
  return (
    <SearchProvider config={config}>
    <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
      {({ wasSearched }) => (
        <div className="App" style={{ display: "flex" }}>
          {/* Content */}
          <div className="innercontainer" style={{ flex: 1 }}>
            <SearchBox />
            {/* Facets */}
            <div className="sidebar">
              <Facet className="facet" field="age" label="Age" show={999}/>
              <Facet className="facet" field="gender" label="Gender" show={999}/>
              <Facet className="facet" field="accent" label="Accent" show={999}/>
              <Facet className="facet-last" field="duration" label="Duration" show={999}/>
            </div>
            {wasSearched && (
              <>
                <PagingInfo />
                <Results resultView={CustomResultView} />
                {/* <Results /> */}
                <Paging />
              </>
            )}
          </div>
        </div>
      )}
    </WithSearch>
  </SearchProvider>
  );
}
