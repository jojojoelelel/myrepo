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

// Initialise connector to Elasticsearch service
const connector = new ElasticsearchAPIConnector({
  host: "http://3.107.8.57:9200", // public ip
  index: "cv-transcriptions",
});

// Set config for Elasticsearch SearchProvider
const config = {
  // Searchable fields : generated_text, duration, age, gender, accent
  searchQuery: {
    // Only generated_text is text input searchable
    search_fields: {
      generated_text: { weight : 3},
    },
    // To retrieve the raw/original values of the fields
    result_fields: {
      generated_text: { raw: {} },
      duration: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} },
    },
    // Facets are used to filter search by age, gender, accent and duration
     facets: {
      age: { type: 'value' },
      gender: { type: 'value' },
      accent: { type: 'value' },
      duration: {
        // duration is a range field with the following ranges
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
  // Immediately search when the page is loaded
  alwaysSearchOnInitialLoad: true,
  // Use the connector to connect to Elasticsearch service
  apiConnector: connector,
};

// The result view that displays the search results
const ResultView = ({ result }) => (
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
    // SearchProvider is the main component
    <SearchProvider config={config}>
      {/* WithSearcg provides search context */}
    <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
      {({ wasSearched }) => (
        // Main container
        <div className="App" style={{ display: "flex" }}>
          {/* Content container that holds the search box, facet bar, results and paging */}
          <div className="innercontainer" style={{ flex: 1 }}>
            {/* Search input box component */}
            <SearchBox />
            {/* Filter facets area */}
            <div className="facetbar">
              {/* Facet components for filtering by different fields */}
              {/* show={999} to show all available values */}
              <Facet className="facet" field="age" label="Age" show={999}/>
              <Facet className="facet" field="gender" label="Gender" show={999}/>
              <Facet className="facet" field="accent" label="Accent" show={999}/>
              <Facet className="facet-last" field="duration" label="Duration" show={999}/>
            </div>
            {/* Only show results section after a search has been performed */}
            {wasSearched && (
              <>
              {/* Shows current page and total results information */}
                <PagingInfo />
                {/* Displays the search results with ResultView component */}
                <Results resultView={ResultView} />
                {/* Pagination controls to navigate through results */}
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
