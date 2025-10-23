
// ============================================
// FILE: src/controllers/dataController.js
// ============================================
const Post = require('../models/Post');
const { ApiResponse } = require('../utils/apiResponse');

exports.createPost = async (req, res, next) => {
  try {
    const { title, content, tags, category } = req.body;
    
    const post = await Post.create({
      title,
      content,
      tags,
      category,
      author: req.user.id
    });

    res.status(201).json(
      ApiResponse.success({ post }, 'Post created successfully')
    );
  } catch (error) {
    next(error);
  }
};

exports.getAllPosts = async (req, res, next) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const skip = (page - 1) * limit;
    const { category, status } = req.query;

    const filter = {};
    if (category) filter.category = category;
    if (status) filter.status = status;

    const posts = await Post.find(filter)
      .populate('author', 'name email')
      .limit(limit)
      .skip(skip)
      .sort({ createdAt: -1 });

    const total = await Post.countDocuments(filter);

    res.status(200).json(
      ApiResponse.success({
        posts,
        pagination: {
          page,
          limit,
          total,
          pages: Math.ceil(total / limit)
        }
      }, 'Posts retrieved successfully')
    );
  } catch (error) {
    next(error);
  }
};

exports.getPostById = async (req, res, next) => {
  try {
    const post = await Post.findById(req.params.id)
      .populate('author', 'name email avatar');
    
    if (!post) {
      return res.status(404).json(
        ApiResponse.error('Post not found')
      );
    }

    // Increment views
    post.views += 1;
    await post.save();

    res.status(200).json(
      ApiResponse.success({ post }, 'Post retrieved successfully')
    );
  } catch (error) {
    next(error);
  }
};

exports.updatePost = async (req, res, next) => {
  try {
    const { title, content, tags, category, status } = req.body;
    
    const post = await Post.findById(req.params.id);
    
    if (!post) {
      return res.status(404).json(
        ApiResponse.error('Post not found')
      );
    }

    // Check if user is the author
    if (post.author.toString() !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json(
        ApiResponse.error('Not authorized to update this post')
      );
    }

    post.title = title || post.title;
    post.content = content || post.content;
    post.tags = tags || post.tags;
    post.category = category || post.category;
    post.status = status || post.status;

    await post.save();

    res.status(200).json(
      ApiResponse.success({ post }, 'Post updated successfully')
    );
  } catch (error) {
    next(error);
  }
};

exports.deletePost = async (req, res, next) => {
  try {
    const post = await Post.findById(req.params.id);
    
    if (!post) {
      return res.status(404).json(
        ApiResponse.error('Post not found')
      );
    }

    // Check if user is the author
    if (post.author.toString() !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json(
        ApiResponse.error('Not authorized to delete this post')
      );
    }

    await post.deleteOne();

    res.status(200).json(
      ApiResponse.success(null, 'Post deleted successfully')
    );
  } catch (error) {
    next(error);
  }
};

exports.likePost = async (req, res, next) => {
  try {
    const post = await Post.findById(req.params.id);
    
    if (!post) {
      return res.status(404).json(
        ApiResponse.error('Post not found')
      );
    }

    const likeIndex = post.likes.indexOf(req.user.id);
    
    if (likeIndex > -1) {
      // Unlike
      post.likes.splice(likeIndex, 1);
    } else {
      // Like
      post.likes.push(req.user.id);
    }

    await post.save();

    res.status(200).json(
      ApiResponse.success({ 
        likes: post.likes.length,
        isLiked: likeIndex === -1
      }, 'Post like status updated')
    );
  } catch (error) {
    next(error);
  }
};
