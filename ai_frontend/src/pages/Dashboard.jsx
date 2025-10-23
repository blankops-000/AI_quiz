import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="dashboard">
      <div className="container">
        <h1>Welcome to your Dashboard, {user?.name}!</h1>
        
        <div className="dashboard-grid">
          <div className="dashboard-card">
            <h3>Create New Post</h3>
            <p>Share your thoughts with the community</p>
            <Link to="/create-post" className="btn btn-primary">
              Create Post
            </Link>
          </div>
          
          <div className="dashboard-card">
            <h3>AI Assistant</h3>
            <p>Get help from our AI assistant</p>
            <Link to="/ai-assistant" className="btn btn-primary">
              Open AI Assistant
            </Link>
          </div>
          
          <div className="dashboard-card">
            <h3>Your Profile</h3>
            <p>Manage your account settings</p>
            <Link to="/profile" className="btn btn-primary">
              View Profile
            </Link>
          </div>
          
          <div className="dashboard-card">
            <h3>Browse Posts</h3>
            <p>Explore posts from other users</p>
            <Link to="/posts" className="btn btn-primary">
              Browse Posts
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;