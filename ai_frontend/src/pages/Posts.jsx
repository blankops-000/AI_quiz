import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import dataService from '../services/dataService';

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true);
        const data = await dataService.getAllPosts({ status: 'published' });
        setPosts(data.posts || []);
      } catch (err) {
        console.error('Error fetching posts:', err);
        setError('Failed to load posts');
        // Fallback to mock data if API fails
        const mockPosts = [
          {
            _id: '1',
            title: 'Getting Started with React',
            content: 'React is a powerful JavaScript library for building user interfaces...',
            author: { name: 'John Doe' },
            createdAt: '2024-01-15'
          },
          {
            _id: '2',
            title: 'Understanding Node.js',
            content: 'Node.js is a runtime environment that allows you to run JavaScript on the server...',
            author: { name: 'Jane Smith' },
            createdAt: '2024-01-14'
          }
        ];
        setPosts(mockPosts);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (loading) {
    return <div className="loading">Loading posts...</div>;
  }

  return (
    <div className="posts-page">
      <div className="container">
        <div className="posts-header">
          <h1>All Posts</h1>
          <Link to="/create-post" className="btn btn-primary">
            Create New Post
          </Link>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="posts-grid">
          {posts.map(post => (
            <div key={post._id} className="post-card">
              <h3>
                <Link to={`/posts/${post._id}`}>{post.title}</Link>
              </h3>
              <p className="post-excerpt">
                {post.content.substring(0, 150)}...
              </p>
              <div className="post-meta">
                <span>By {post.author?.name || 'Unknown'}</span>
                <span>{new Date(post.createdAt).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Posts;