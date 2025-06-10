import React, { useEffect, useState } from 'react'
import NewsItem from './NewsItem'
import Spinner from './Spinner'
import PropTypes from 'prop-types'
import Pagination from './Pagination';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';





// import { useEffect } from 'react'
export default function News(props) {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  // constructor(){
  //   super();
  //   console.log("hello I am a constructor from news component");
  //   this.state={
  //     articles:this.articles,
  //    page:0,
  //    loading:false
  //   }
 
//businessentertainmentgeneralhealthsciencesportstechnology
//componentDidMount is used to do any thing like fetch data or api just after the rendering of components on dom
const updatenews = async () => {
  setLoading(true);
  props.setProgress(10);
  const url = `https://google-news13.p.rapidapi.com/${props.category}?lr=en-US`;
  const options = {
    method: 'GET',
    headers: {
      'x-rapidapi-key': `${props.apiKey}`,
      'x-rapidapi-host': 'google-news13.p.rapidapi.com'
    }
  };

  try {
    const response = await fetch(url, options);
    // props.setProgress(40);
    const data = await response.json();
    console.log(data);
    props.setProgress(70);
    const items = data.items; // Assuming 'items' contains the articles
    const totalResults = items.length;
    setArticles(items);
    setTotalResults(totalResults);
    setLoading(false);
   
    props.setProgress(100);
  
  } catch (error) {
    console.error(error);
  }
}
//hello
useEffect(() => {
  updatenews()
}, [])


useEffect(() => {
  scrollToTop();
}, [page]);

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth' // Smooth scrolling effect
  });
}

const handleNextClick1 = async () => {
  console.log("next");
 setPage((prevPage)=>{
const newPage=prevPage+props.pagesize;
scrollToTop();
return newPage;
 })
}
const handlePrevCick1 = async () => {
  console.log("prev");

  // this.setState(
  //   (prevState) => ({ page: prevState.page - props.pagesize }),
  //   () => {
  //     this.scrollToTop(); // Ensures scroll happens after state update
  //     console.log(this.state.page, "Current Page after Prev Click");
  //   }
  // );
  setPage((prevPage) => {
    const newPage = prevPage - props.pagesize;
    scrollToTop(); // Ensure scroll happens after state update
    console.log(newPage, "Current Page after Prev Click");
   return newPage;
  });
};
console.log("render");

 
return (
  <div className='container main' >
    <h2 className='text-center my-4 heading'>GlobeGaze Top HeadLines</h2>
    {loading && <Spinner />}

    <div className="row">
      <Pagination items={articles} page={page} loading={loading} />
    </div>
    <div className="container my-4 d-flex justify-content-around" >
      <button disabled={page - props.pagesize < 0} type="button" className="btn btn-dark" onClick={handlePrevCick1}>&larr; Previous</button>
      <button type="button" disabled={page + props.pagesize >= articles.length} className="btn btn-dark" onClick={handleNextClick1}>Next &rarr;</button>
    </div>
  </div>
)
}


News.defaultProps = {
  country: "us",
  pagesize: 6,
  category: "general"
}
News.propTypes = {
  country: PropTypes.string,
  pagesize: PropTypes.number,
  category: PropTypes.string
}


