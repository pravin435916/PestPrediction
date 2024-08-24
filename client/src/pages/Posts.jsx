import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Rating } from '@mui/material';

const Posts = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/posts');
        
        // Log the response structure for clarity
        console.log('API response:', response.data);

        // Extract posts from the data field
        const postsArray = response.data.data;

        if (Array.isArray(postsArray)) {
          setPosts(postsArray);
        } else {
          console.error('The posts data is not an array:', postsArray);
          setPosts([]); // Fallback to an empty array
        }
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };

    fetchPosts();
  }, []);

  return (
    <div className="container mx-auto mt-8">
      <h1 className="text-3xl font-bold mb-4">Posts</h1>
      <div className="grid grid-cols-3 gap-4">
        {posts.map(post => (
          <div key={post._id} className="bg-white p-4 rounded-lg shadow-md">
            <h2 className="text-lg font-semibold mb-2">@{post.name}</h2>
            <div className="mb-4">
              <Rating name={`rating-${post._id}`} value={post.rating || 0} readOnly />
            </div>
            <p>{post.msg}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Posts;
