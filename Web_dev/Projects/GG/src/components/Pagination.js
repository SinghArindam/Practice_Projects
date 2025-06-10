import React, { Component } from 'react'
import NewsItem from './NewsItem'
export default function Pagination (props){
  
    let ind=0;
    return (
        <div className='row my-4'>
                  {
                  !props.loading && props.items  && props.items.slice(props.page, props.page+6).map((ele)=>{
                    let des;
                    let pre;
                    let t;
                    let img;
                    // let ind=0;
                if(ele!=undefined || ele!=null){
                 
                   pre=ele.snippet;
                
                  if(pre!=null && pre.length>35){
                   des= pre.substring(0,36)+"...";
                }
                if(ele.title!=null && ele.title.length>30){
                  t=ele.title.substring(0,31)+"...";
                }
                if(ele.images===undefined || ele.images['thumbnailProxied']===undefined){
                  img='https://cdn.pixabay.com/photo/2017/06/26/19/03/news-2444778_1280.jpg';
                }else{
                  img=ele.images['thumbnailProxied'];
                }
                
                return <div className="col-md-4" key={ind++}>
                <NewsItem  title={t} description={des} imageUrl={img} newsUrl={ele.newsUrl}/>
                </div>

                }
                 
                })}
              </div>
    )
  
}




// import React, { Component } from 'react'
// import NewsItem from './NewsItem';
// export default class pagination extends Component {

//     constructor(){
//         super();
//         // console.log("hello I am a constructor from news component");
//         this.state={
//           articles:this.articles,
//          index:6,
//          loading:false
    
//         }
        
//       }
//   render() {
//     return (
//       <div>
//          {!this.state.loading && this.state.articles.map((ele)=>{
//           let des;
//           let pre=ele.preview;
//           if(pre!=null && pre.length>35){
//            des= pre.substring(0,36)+"...";
//         }let t;
//         if(ele.title!=null && ele.title.length>30){
//           t=ele.title.substring(0,31)+"...";
//         }
//           return <div className="col-md-4" key={ele.url}>
//             <NewsItem  title={t} description={des} imageUrl={ele.image} newsUrl={ele.link}/>
//             </div>
//         })}
//       </div>
//     )
//   }
// }
