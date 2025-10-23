import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import dataService from '../services/dataService';

const PostDetail = () => {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPost = async () => {
      try {
        setLoading(true);
        const data = await dataService.getPostById(id);
        setPost(data.post);
      } catch (err) {
        console.error('Error fetching post:', err);
        setError('Failed to load post');
        // Fallback to mock data if API fails
        const mockPost = {
          _id: id,
          title: 'Getting Started with React',
          content: `React is a powerful JavaScript library for building user interfaces. It was developed by Facebook and has become one of the most popular frontend frameworks.

Here are some key concepts:

1. Components - Reusable pieces of UI
2. JSX - JavaScript XML syntax
3. State - Component data that can change
4. Props - Data passed to components
5. Hooks - Functions that let you use state and lifecycle features

React makes it easy to create interactive UIs with its component-based architecture.`,
          author: { name: 'John Doe' },
          createdAt: '2024-01-15'
        };
        setPost(mockPost);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [id]);

  if (loading) {
    return <div className="loading">Loading post...</div>;
  }

  if (!post) {
    return <div className="error">Post not found</div>;
  }

  return (
    <div className="post-detail">
      <div className="container">
        <Link to="/posts" className="back-link">← Back to Posts</Link>
        
        {error && <div className="error-message">{error}</div>}
        
        <article className="post">
          <header className="post-header">
            <h1>{post.title}</h1>
            <div className="post-meta">
              <span>By {post.author?.name || 'Unknown'}</span>
              <span>{new Date(post.createdAt).toLocaleDateString()}</span>
            </div>
          </header>
          
          <div className="post-content">
            {post.content.split('\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>
        </article>
      </div>
    </div>
  );
};

export default PostDetail;